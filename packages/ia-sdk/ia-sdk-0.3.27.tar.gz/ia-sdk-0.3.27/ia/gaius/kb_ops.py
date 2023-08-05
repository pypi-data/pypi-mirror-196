"""Provides utilities for higher level operations on KnowledgeBases"""
from ia.gaius.agent_client import AgentClient
from collections import Counter


def list_models(agent: AgentClient, nodes=None):
    """Return a dict of {node_name: model_list} found on specified nodes

    Args:
        agent (AgentClient): GAIuS Agent
        nodes (list, optional): nodes to list models on

    Returns:
        dict: {node_name: model_list} for each node specified in nodes

    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.kb_ops import list_models

            agent = AgentClient(agent_info)

            #get list of models found on node P1
            models = list_models(agent, nodes=['P1'])

    """
    if not agent._connected:
        agent.connect()

    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        models_dict = {k: list(v['models_kb'].keys()) for k, v in kb.items()}

    except Exception as e:
        print(f'Error in list_models: {e}')
        raise e
    finally:
        agent.set_summarize_for_single_node(prev_summarize_state)

    return models_dict


def list_symbols(agent: AgentClient, nodes=None):
    """Return a dict of {node_name: symbol_list} found on specified nodes

    Args:
        agent (AgentClient): GAIuS Agent
        nodes (list, optional): nodes to list symbols on

    Returns:
        dict: {node_name: symbol_list} for each node specified in nodes

    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.kb_ops import list_symbols

            agent = AgentClient(agent_info)

            #get list of symbols found on node P1
            symbols = list_symbols(agent, nodes=['P1'])

    """
    if not agent._connected:
        agent.connect()

    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        symbols_dict = {k: list(v['symbols_kb'].keys()) for k, v in kb.items()}
    except Exception as e:
        print(f'Error in list_symbols: {e}')
        raise e
    finally:
        agent.set_summarize_for_single_node(prev_summarize_state)

    return symbols_dict


def get_models_containing_symbol(agent: AgentClient, symbol_set: set, nodes=None):
    """Checks for presence of symbols from `symbol_set` in each model on `nodes`, adding to return dict if a symbol is found.

    Args:
        agent (AgentClient): GAIuS Agent
        symbol (str): the symbol to search for
        nodes (_type_, optional): nodes to search. Defaults to searching all nodes

    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.kb_ops import get_models_containing_symbol

            symbols = ["world"]
            agent = AgentClient(agent_info)

            output = get_models_containing_symbol(agent=agent, symbol_set=set(symbols))
    """

    if not agent._connected:
        agent.connect()

    sym_dict = {}
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)

        for node, node_kb in kb.items():
            sym_dict[node] = set()
            if 'models_kb' not in node_kb:
                continue
            for model_name, model in node_kb['models_kb'].items():
                for event in model['sequence']:
                    for sym in event:
                        if sym in symbol_set:
                            sym_dict[node].add(model_name)

    except Exception as e:
        print(f'Error in identify_models_with_symbol: {e}')
        raise e
    finally:
        agent.set_summarize_for_single_node(prev_summarize_state)

    return sym_dict


def get_models_containing_symbol_strict(agent: AgentClient, symbol_set: set, nodes=None):
    """Checks for presence of symbols from `symbol_set` in each model on `nodes`.
    Only adds model to return dict if all symbols in model are from symbol set
    Store as a dict of {node_name : list}

    Args:
        agent (AgentClient): GAIuS Agent
        symbol (str): the symbol to search for
        nodes (_type_, optional): nodes to search. Defaults to searching all nodes


    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.kb_ops import get_models_containing_symbol_strict

            symbols = ["hello", "world", "goodbye", "cruel"]
            agent = AgentClient(agent_info)

            output = get_models_containing_symbol_strict(agent=agent, symbol_set=set(symbols))

    """

    if not agent._connected:
        agent.connect()

    sym_dict = {}
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)

        for node, node_kb in kb.items():
            sym_dict[node] = set()
            if 'models_kb' not in node_kb:
                continue
            for model_name, model in node_kb['models_kb'].values():
                unique_symbols_in_model = set()
                for event in model['sequence']:
                    for sym in event:
                        unique_symbols_in_model.add(sym)

                if all([sym in symbol_set for sym in unique_symbols_in_model]):
                    sym_dict[node].add(model_name)

    except Exception as e:
        print(f'Error in identify_models_with_symbol: {e}')
        raise e
    finally:
        agent.set_summarize_for_single_node(prev_summarize_state)

    return sym_dict


def get_kb_subset(agent: AgentClient, model_dict: dict):
    """Retrieve a subset of a Knowledgebase based on the provided model_dict.
    Will only provide used symbols and vectors, all others will be trimmed.

    Args:
        agent (AgentClient): GAIuS Agent
        model_dict (dict): {node_name: model_list}. Expected format is similar to that returned from :func:`list_models`

    Raises:
        e: Exception in subset iteration (e.g. model not found on node, get_kb failed, etc.)

    Returns:
        dict: Subset of Knowledgebases corresponding to provided model_dict

    Example:
        .. code-block:: python
            :force:

            from ia.gaius.kb_ops import get_kb_subset, list_models
            from ia.gaius.agent_client import AgentClient

            agent = AgentClient(agent_info)
            agent.connect()

            models = list_models(agent=agent, nodes=['P1'])

            # get a subset of available models
            models = {k: v[:20] for k,v in models.items()}

            # get a subset of the entire Knowledgebase
            kb_subset = get_kb_subset(agent=agent, model_dict=models)

    """

    try:
        reconstructed_kb = {}
        for node, models in model_dict.items():

            node_kb = agent.get_kbs_as_json(obj=True, nodes=[node], ids=False)
            node_kb = node_kb[node]

            if not all([model in node_kb["models_kb"] for model in models]):
                print(f'Not all models were found on node {node}')
                for model in models:
                    if model not in node_kb["models_kb"]:
                        print(f'model "{model}" not found')
                raise Exception(f'Not all models were found on node {node}')

            reconstructed_kb[node] = {'models_kb': {},
                                      'symbols_kb': {},
                                      'vectors_kb': {},
                                      'metadata': {}}
            print(f'original model count: {len(node_kb["models_kb"])}')
            print(f' reduced model count: {len(models)}')
            # will need to recompute symbol frequency and model member frequency counts
            symbol_freq_counter = Counter()
            symbol_model_member_freq_counter = Counter()

            # only keep symbols found in the specified models for the kb subset
            symbol_set = set()
            for model in models:
                unique_symbols_in_model = set()
                reconstructed_kb[node]["models_kb"][model] = node_kb["models_kb"][model]
                for event in reconstructed_kb[node]["models_kb"][model]['sequence']:
                    for sym in event:
                        symbol_set.add(sym)
                        unique_symbols_in_model.add(sym)
                    symbol_freq_counter.update(event)

                symbol_model_member_freq_counter.update(unique_symbols_in_model)

            for sym in symbol_set:
                reconstructed_kb[node]['symbols_kb'][sym] = node_kb['symbols_kb'][sym]

                # update frequency and model member frequency to new subset values
                reconstructed_kb[node]['symbols_kb'][sym]['features']['frequency'] = symbol_freq_counter[sym]
                reconstructed_kb[node]['symbols_kb'][sym]['features']['model_member_frequency'] = symbol_model_member_freq_counter[sym]

                # if the symbol is a vector, add it to the subset vectors_kb
                if 'VECTOR|' in sym:
                    vectHash = sym.split('|')[-1]
                    reconstructed_kb[node]['vectors_kb'][vectHash] = node_kb['vectors_kb'][vectHash]

        return reconstructed_kb
    except Exception as e:
        print(f'failed to retrieve kb subset: {e}')
        raise e


def recursive_delete_model(agent: AgentClient, model_name: str, nodes=None, log_to_file: bool = False):
    """Recursively remove a model from an Agent.

    Args:
        agent (AgentClient): _description_
        model_name (str): _description_
        nodes (_type_, optional): _description_. Defaults to None.
        log_to_file (bool, optional): _description_. Defaults to False.
    """

    if not agent._connected:
        return "Agent not connected"

    if log_to_file:
        import time
        t = time.localtime()
        file = open(f"{time.strftime('recursive_model_delete_log_%Y_%m_%d_%H_%M_%S', t)}_log.txt", mode='w+')
    
    # variables
    changed_models = {}
    primitve_patterns_to_remove = []
    symbols_to_update_in_other_nodes = {}
    
    if nodes is None:
        nodes = agent.all_nodes
    else:
        nodes = [node for node in agent.all_nodes if (node['name'] in nodes)]

    overall_result = {}
    
    for node in nodes:
        changed_models[node["name"]] = dict()
    
    for node in nodes:
        try:
            # call delete model on the passed nodes
            response = agent.delete_model(model_name, [node["name"]])
            overall_result[node["name"]] = response[node["name"]]
            
            if(log_to_file):
                file.write(f"initial delete_model response = {response}")
            
            # if model not in node, need to look for patterns
            # else add the pattern with the passed model name to primitve_patterns_to_remove 
            if(response[node["name"]] != "deleted"):
                if(log_to_file):
                    file.write("Trying to recursive delete models")
                for pattern in primitve_patterns_to_remove:
                    if(log_to_file):
                        file.write(f"Looking for pattern {pattern} in {node['name']}")
                    result = agent.remove_patterns_from_system([pattern])

                    # go through nodes again to make sure that pattern gets removed
#                         print(f"result = {result}")
#                         print(f"result.keys() = {result.keys()}")
                    if result == {}:
                        continue

                    for node1 in nodes:
                        if(log_to_file):
                            file.write(f"node1 = {node1['name']}")
                        # if nothing was found, then go to next pattern
                        if(log_to_file):
                            file.write(f"result[{node1['name']}] = {result[node1['name']] if (result[node1['name']] == {}) else result[node1['name']]['models']}")
                        
                        if(result[node1["name"]] == {}):
                            continue

                        for old_model_hash, new_model_hash in result[node1["name"]]["models"].items():
                            # so if that caused a model to be deleted, add this model
                            # to list of patterns to remove

                            # else update models further 
                            if(new_model_hash == "deleted"):
                                if(log_to_file):
                                    file.write(f"Adding .+\|{node1['id']}\|{old_model_hash}.+ to primitve_patterns_to_remove")
                                
                                pattern = f".+\|{node1['id']}\|{old_model_hash}.+"

                                # don't add the pattern if its already there
                                if pattern in primitve_patterns_to_remove:
                                    continue

                                primitve_patterns_to_remove.append(f".+\|{node1['id']}\|{old_model_hash}.+")
                                changed_models[node1["name"]][old_model_hash] = "deleted"
                            else:
                                if(log_to_file):
                                    file.write(f"Adding .+\|{node1['id']}\|{old_model_hash}.+ to symbols_to_update_in_other_nodes")
                                pattern = f".+{old_model_hash}.+"
                                # don't add the pattern if its already there
                                if pattern in symbols_to_update_in_other_nodes:
                                    continue

                                symbols_to_update_in_other_nodes[f".+{old_model_hash}.+"] = new_model_hash
                                changed_models[node1["name"]][old_model_hash] = new_model_hash
                    
                if(log_to_file):
                    file.write(f"Updating symbols")
                
                for old_symbol, new_symbol in symbols_to_update_in_other_nodes.items():
                    '''
                    Steps:
                        1) Get models which contain an old symbol
                        2) Get their sequences
                        3) Replace the symbol in their sequences with the new one
                        4) Delete old model
                        5) Add new model
                        6) Add record to symbols_to_update_in_other_nodes with old_model
                    '''
                    # get all models with pattern that needs to be updated
                    models_with_pattern = agent.get_models_with_patterns([old_symbol])

                    for node1 in nodes:
                        if (log_to_file):
                            file.write(f"models_with_pattern[{node1['name']}] = {models_with_pattern[node1['name']]} with {old_symbol}")

                        if (models_with_pattern[node1["name"]]["model_list"] == []):
                            continue

                        if (log_to_file):
                            file.write("node1['name'] not an empty list")

                        # go through each of them and delete the old model
                        # and add a model with the new symbol
                        for model in models_with_pattern[node1["name"]]["model_list"]:
                            model_instance = agent.get_model(model, nodes=[node1['name']])
                            if model_instance[node1["name"]] == {}:
                                continue


                            model_sequence = model_instance[node1["name"]]["sequence"]
                            model_frequency = model_instance[node1["name"]]["frequency"]
                            model_emotives = model_instance[node1["name"]]["emotives"]

                            # delete the model
                            response = agent.delete_model(model)
                            if (log_to_file):
                                file.write(f"response to delete_model[{node1['name']}] = {response[node1['name']]} for model = {model}")

                            # don't continue unless it was actually deleted
                            if(response[node1["name"]] != "deleted"):
                                if (log_to_file):
                                    file.write(f"{response[node1['name']]}")
                                continue
                            else:
                                if (log_to_file):
                                    file.write(f"delete old model response = {response}")

                            # replace patterns
                            pure_hash = old_symbol
                            pure_hash = pure_hash.replace(".+", "")
                            for i in range(0, len(model_sequence)):
                                for j in range(0, len(model_sequence[i])):
                                    if (pure_hash in model_sequence[i][j]):
                                        if (log_to_file):
                                            file.write(f"replaced {model_sequence[i][j]} with {new_symbol}")
                                        model_sequence[i][j] = model_sequence[i][j].replace(pure_hash, new_symbol)

                            # add model with new symbols
                            response = agent.add_model(sequence = model_sequence,
                                            vector=[],
                                            frequency = model_frequency,
                                            emotives = model_emotives,
                                            nodes=[node1['name']])

                            if (log_to_file):
                                file.write(f"response to add_model = {response}")

                            changed_models[node1["name"]][model] = response[node1["name"]]["name"]

            else:
                if (log_to_file):
                    file.write(f"Added .+\|{node['id']}\|{model_name}.+ pattern to primitve_patterns_to_remove")
                primitve_patterns_to_remove.append(f".+\|{node['id']}\|{model_name}.+")
        
        except Exception as exception:
            raise str(exception)

    if (log_to_file):
        file.close()

    # TODO changed models can be returned, but becomes super messy if you update a model several times
    return overall_result, changed_models


def recursive_update_model(agent: AgentClient, model_name: str,
                           model: dict = {}, nodes = None, log_to_file: bool = False):
    """_summary_
    Args:
        agent (AgentClient): _description_
        model_name (str): _description_
        nodes (_type_, optional): _description_. Defaults to None.
        log_to_file (bool, optional): _description_. Defaults to False.
    """

    if (not agent._connected):
        return "Agent not connected"

    if (log_to_file):
        import time
        t = time.localtime()
        file = open(f"{time.strftime('recursive_model_update_log_%Y_%m_%d_%H_%M_%S', t)}_log.txt", mode='w+')

    # variables
    changed_models = {}
    primitve_patterns_update_in_other_nodes = {}

    if nodes is None:
        nodes = agent.all_nodes
    else:
        nodes = [node for node in agent.all_nodes if (node['name'] in nodes)]

    overall_result = {}

    for node in nodes:
        changed_models[node["name"]] = dict()

    for node in nodes:
        try:
            # call delete model on the passed nodes
            response = agent.update_model(model_name, model, [node["name"]])
            overall_result[node["name"]] = response[node["name"]]

            if (log_to_file):
                file.write(f"initial update_model response = {response[node['name']]}\n")

            # if model was not in node, just skip
            if (response[node['name']].find("failed") != -1):
                continue

            changed_models[node["name"]] = response[node["name"]]

            # if model_hash did not change, we can simple add it to the list of symbols to update
            file.write(f"{model=}")
            model["name"] = response[node['name']]
            primitve_patterns_update_in_other_nodes[f".+\|{node['id']}\|{model_name}.+"] = model

            if (log_to_file):
                file.write("Trying to recursive update models\n")

            for node1 in nodes:
                # current node won't contain a pattern its updated
                if (node1 == node):
                    continue

                patterns_to_add = {}
                for pattern, pattern_data in primitve_patterns_update_in_other_nodes.items():
                    if (log_to_file):
                        file.write(f"Looking for pattern {pattern} in {node1['name']}\n")
                    # need to get all models that contain this model in their sequences
                    result = agent.get_models_with_patterns([pattern], [node1["name"]])[node1["name"]]["model_list"]

                    if (log_to_file):
                        file.write(f"Result for {pattern} in {node1['name']} {result=}\n")

                    if (result == []):
                        continue

                    model_name_to_find = pattern.split("|")[-1][0:-2]
                    if (log_to_file):
                        file.write(f"{model_name_to_find=}")

                    # for each model that needs to be updated, we update
                    for model_name in result:
                        # get model data
                        model_data = agent.get_model(model_name)[node1["name"]]

                        # find where the model name appears and replace it
                        for i in range(len(model_data["sequence"])):
                            for j in range(len(model_data['sequence'][i])):
                                if (model_data["sequence"][i][j].find(model_name_to_find) != -1):
                                    model_data["sequence"][i][j] = \
                                        model_data["sequence"][i][j].replace(model_name_to_find, pattern_data["name"])

                        # convert emotives in model_data and average it
                        for key, item in model_data["emotives"].items():
                            emotive_data = model_data["emotives"][key]
                            if not (type(emotive_data) is list):
                                continue

                            model_data["emotives"][key] = sum(emotive_data) / len(emotive_data)

                        # replace emotive values (no way to really average it)
                        for key, item in pattern_data["emotives"].items():
                            model_data["emotives"][key] = item

                        # replace metadata
                        model_data["metadata"] = pattern_data["metadata"]

                        # replace pattern with new data
                        recur_result = agent.update_model(model, model_data, [node1["name"]])[node1["name"]]

                        # add updated pattern
                        changed_models[node1["name"]][model_data["name"]] = recur_result
                        model_data["name"] = recur_result
                        if (pattern in patterns_to_add):
                            continue
                        patterns_to_add[f".+\|{node1['id']}\|{model_name}.+"] = model_data

                for pattern, pattern_data in patterns_to_add.items():
                    # add updated pattern
                    if (pattern in primitve_patterns_update_in_other_nodes):
                        continue
                    primitve_patterns_update_in_other_nodes[pattern] = pattern_data

        except Exception as exception:
            raise str(exception)

    if (log_to_file):
        file.close()

    # TODO changed models can be returned, but becomes super messy if you update a model several times
    return overall_result, changed_models
