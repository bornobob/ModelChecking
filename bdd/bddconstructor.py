from bdd.nodes import BasicEventNode, LeafNode
from bdd.bdd import BDD
from bdd.bddminimiser import BDDMinimiser


class BDDConstructor:
    """
    The BDDConstructor can translate a Fault Tree into a BDD.
    """

    def __init__(self, fault_tree):
        """
        Constructor for the BDDConstructor. Takes as an argument
        the fault tree to be converted.
        """
        self._fault_tree = fault_tree

    def construct_bdd(self, ordering, minimise=True):
        """
        Constructs a BDD with the given ordering.
        :param ordering: The ordering to use for the construction.
        :param minimise: Whether or not to minimise the BDD after
                         construction.
        :return: the created system.
        """
        var_ordering = ordering.order_variables(self._fault_tree)
        bdd = BDD(self._construct_bdd(
            var_ordering,
            self._fault_tree.get_false_state()
        ))
        if minimise:
            return BDDMinimiser(bdd).minimise()
        else:
            return bdd

    def _construct_bdd(self, variable_ordering, state):
        """
        The construct_bdd function takes the remaining variable
        ordering and the current state to create a new layer
        of the final BDD.
        This function works depth first.
        """
        self._fault_tree.set_states(state)
        fault_tree_holds = self._fault_tree.apply()
        if fault_tree_holds or not variable_ordering:
            return LeafNode(fault_tree_holds)
        else:
            return self._construct_node(
                variable_ordering[0],
                variable_ordering[1:],
                state
            )

    def _construct_node(self, variable, variable_ordering, state):
        """
        Construct_node is a helper function to create the entire BDD.
        It constructs a non-leaf-node.
        """
        state[variable] = True
        true_node = self._construct_bdd(variable_ordering, state)
        state[variable] = False
        false_node = self._construct_bdd(variable_ordering, state)
        return BasicEventNode(
            true_node,
            false_node,
            self._fault_tree.get_basic_event(variable)
        )

    def construct_bdd_test(self, variable_ordering):
        """
        Construct BDD with literal variable ordering (instead of an
        Ordering class).
        USE ONLY FOR TESTING!
        :param variable_ordering:
        :return: The constructed BDD.
        """
        false_state = self._fault_tree.get_false_state()
        return BDD(self._construct_bdd(variable_ordering, false_state))
