import libcst as cst


class PrintTransformer(cst.CSTTransformer):
    def leave_SimpleStatementLine(self, node, updated_node):
        if isinstance(node, cst.SimpleStatementLine):
            for n in node.body:
                if is_print_statement(n):
                    return cst.RemovalSentinel.REMOVE

        return node


def is_print_statement(n) -> bool:
    if (
        isinstance(n, cst.Expr)
        and isinstance(n.value, cst.Call)
        and isinstance(n.value.func, cst.Name)
        and n.value.func.value == "print"
    ):
        return True
    else:
        return False
