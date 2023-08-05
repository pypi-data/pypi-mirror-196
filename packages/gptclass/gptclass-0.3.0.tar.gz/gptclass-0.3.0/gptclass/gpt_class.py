from .function_utils import function_explainer, function_caller


class Explainer:
    def __getattr__(self, name: str):
        return function_explainer(name)


class GPTClass:
    @property
    def explain(self) -> Explainer:
        """Prints the code of the generated method
        Example: `GPTClass().explain.add(4, 5)`

        :return: None
        :rtype: None
        """
        return Explainer()

    def __getattr__(self, name: str):
        return function_caller(name)
