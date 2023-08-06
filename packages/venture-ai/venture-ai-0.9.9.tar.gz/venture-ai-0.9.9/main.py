from venture import Venture

if __name__ == '__main__':
    v = Venture(openai_api_key='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', 
                captain_email='captain@spaceship.com', 
                extra_role='You are an AI assistant for Toluna Company.',
                cosmos_path='/Users/roy.sadaka/Documents/MachineLearning/test_temp/leslie_cosmos_data/',
                share=False)
    v.launch()