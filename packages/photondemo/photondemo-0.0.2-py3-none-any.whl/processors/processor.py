class PhotonProcessor:

    def __init__(self, provider: str = None, response: dict = None, *args, **kwargs) -> None:
        self.provider = provider
        self.args = args
        self.kwargs = kwargs
        self.response = response
        self.providers = ["openai", "anthropic", "replicate"] 

    def process_openai_response(self, *args, **kwargs) -> None:
        result = self.response.choices[0].text
        return {
            "output": result,
            "provider": "openai",
            "prompt": kwargs["prompt"],
            "model": kwargs["model"],
        }

    def process_provider(self, *args, **kwargs) -> None:
        # Check if provider is valid
        if self.provider not in self.providers:
            raise ValueError(f"Provider must be one of {self.providers}")
        
        if self.provider == "openai":
            return self.process_openai_response(*args, **kwargs)
            # Do something

        return None