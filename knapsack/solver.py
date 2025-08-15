#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from heapq import heappush, heappop


Item = namedtuple("Item", ['index', 'value', 'weight'])

Node = namedtuple("Node", ['value', 'depth', 'upper', 'room', 'state']) # state is string of 0s and 1s, representing which items are taken



def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight

    '''
    greedy version
    '''
    # unit_values = [item.value / item.weight for item in items]
    # item_idx = list(range(len(items)))
    # item_idx.sort(key=lambda x: unit_values[x], reverse=True)

    # for idx in item_idx:
    #     item = items[idx]
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight


    '''
    DP version
    '''
    def dynamic_programming(items, capacity):
        value = 0
        taken = [0]*len(items)
        dp = {(0,i): 0 for i in range(len(items)+1)}
        def get_dp(k,i):
            if (k,i) in dp:
                return dp[k,i]
            if i == 0:
                dp[k, i] = 0
                return 0
            item = items[i-1]
            if item.weight > k:
                return get_dp(k, i-1)
            else:
                dp[k,i] = max(get_dp(k,i-1), get_dp(k-item.weight, i-1) + item.value)
                return dp[k,i]

        best_value = get_dp(capacity, len(items))
        # print(dp)
        value = best_value
        # print(best_value)
        k = capacity
        j = len(items) - 1

        while j > -1 and k > 0:
        # for j in range(len(items)-1, 0, -1):
            if (k, j) not in dp:
                j -= 1
                continue
            if best_value == dp[k,j]:
                j -= 1
                continue
            k -= items[j].weight
            best_value -= items[j].value
            taken[j] = 1
        
        return value, taken


    def least_discrepancy_search(items, capacity):
        """
        Perform Least Discrepancy Search for the Knapsack problem.
        Args:
            items (list of Item): List of items to consider.
            capacity (int): Maximum knapsack capacity.
        Returns:
            (int, list): Tuple of best value found and list of taken items (0/1).
        """
        # Sort items by value-to-weight ratio (unit value)
        unit_values = [item.value / item.weight for item in items]
        item_idx = list(range(len(items)))
        item_idx.sort(key=lambda x: unit_values[x], reverse=True)

        def greedy_estimate(remain_capacity, remain_items, initial_value=0):
            """
            Estimate upper bound using greedy fill of remaining capacity.
            """
            value = initial_value
            for idx in remain_items:
                item = items[idx]
                if remain_capacity >= item.weight:
                    remain_capacity -= item.weight
                    value += item.value
                else:
                    value += unit_values[idx] * remain_capacity
                    break
            return value

        best_upper = greedy_estimate(capacity, item_idx)

        # Initialize best node and heap (as a max-heap by value)
        best_node = Node(value=0, depth=-1, upper=best_upper, room=capacity, state='0'*len(items))
        # Use a heapq with (-value, ...) for max-heap behavior
        pool = [(-best_node.value, best_node)]


        def greedy_follow(node, item_idx, items, queue: list):
            """
            Greedily take items in order of unit value from the given node.
            Returns the final node and the list of all nodes traversed (excluding the input node).
            """
            current_node = node
            remain_capacity = current_node.room
            j = current_node.depth + 1
            while j < len(items) and remain_capacity > 0:
                item = items[item_idx[j]]
                if remain_capacity < item.weight:
                    break
                remain_capacity -= item.weight
                state = list(current_node.state)
                state[item.index] = '1'
                state = ''.join(state)
                node_new = Node(value=current_node.value + item.value, depth=j, room=remain_capacity, upper=current_node.upper, state=state)
                heappush(queue, (-node_new.value, node_new))
                current_node = node_new
                if node_new.room == 0:
                    break
                j += 1
            return current_node

        # Initial greedy fill
        final_node = greedy_follow(best_node, item_idx, items, pool)
        best_node = final_node

        # Main LDFS loop: explore discrepancies (not following greedy)
        for wave in range(len(items)):
            print("wave: ", wave, " pool size: ", len(pool))
            if len(pool) == 0:
                break
            new_pool = []
            prune_count = 0
            while pool:
                # Pop the node with the highest value (max-heap)
                current_node = heappop(pool)[1]
                # If at leaf node, skip
                if current_node.depth == len(items) - 1:
                    prune_count += 1
                    continue
                # Prune if upper bound is not promising
                if current_node.upper < best_node.value:
                    prune_count += 1
                    continue

                # Move one step not following greedy
                upper = greedy_estimate(current_node.room, item_idx[current_node.depth+2:], current_node.value)
                if upper < best_node.value:
                    prune_count += 1
                    continue
                node = Node(value=current_node.value, depth=current_node.depth+1, room=current_node.room, upper=upper, state=current_node.state)
                heappush(new_pool, (-node.value, node))

                # Follow greedy step from this node
                final_greedy_node = greedy_follow(node, item_idx, items, new_pool)
                if final_greedy_node.value > best_node.value:
                    best_node = final_greedy_node

            pool = new_pool
            print("prune count: ", prune_count)

        value = best_node.value
        taken = [int(i) for i in best_node.state]
        return value, taken

    if capacity * len(items) <= 1e7 or len(items) <= 200:
        value, taken = dynamic_programming(items, capacity)

    else:
        # Call the LDFS function and unpack results
        value, taken = least_discrepancy_search(items, capacity)


    # multi waves, record the current best, upper bound, 

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

