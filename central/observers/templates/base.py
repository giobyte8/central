from abc import ABCMeta, abstractmethod


class Template(metaclass=ABCMeta):

    @abstractmethod
    def render(self, **template_ctx) -> str:
        """Renders template by using passed **kwargs as context \
        for variables inside template.

        Returns:
            str: Context values used to render template
        """
