from venture import Venture

if __name__ == '__main__':
    v = Venture(openai_api_key='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', 
                captain_email='captain@spaceship.com', 
                extra_role='You are an AI assistant for Venture Company.',
                cosmos_path=None,
                share=False)
    v.launch()