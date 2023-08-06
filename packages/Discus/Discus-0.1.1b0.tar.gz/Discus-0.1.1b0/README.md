# Discus-Synthetics

This is a package for generating synthetic datasets to fine-tune LLMs. It uses seed examples, human input, and OpenAI models to generate instructions and instances that can be used to either supplement existing datasets or create completely new datasets.

Review the documentation [here](https://discus.ai/docs/index.html).

## Setup

In order to use this package, you need to first install it.

```bash
pip install discus
```

Set the OpenAI key as an environment variable for security purposes.

```bash
export OPENAI_API_KEY=<your secret key>
```

Now, you can import the package and set the OpenAI key.

```bash
import discus.openai_utils as utils
import discus.instructions as instructions
import discus.instances as instances
import os

utils.set_openai_llm(os.environ["OPENAI_API_KEY"])
```

## Usage

### Generate Instructions

```bash
seed_examples = [
'Write a description of a famous landmark in at least 200 words.',
'Generate a short story that involves time travel and a surprising twist ending.',
'Compose a persuasive essay arguing for the importance of renewable energy sources.',
'Write a step-by-step tutorial on how to bake a chocolate chip cookie.',
'Create a dialogue between two characters discussing the benefits and drawbacks of social media.',
'Generate a list of ten useful productivity tips for managing time effectively.',
'Write a review of a recent movie, including your thoughts on the plot, acting, and cinematography.',
'Compose a letter of recommendation for a coworker highlighting their skills and accomplishments.',
'Write a speech on the importance of mental health and strategies for self-care.',
'Generate a poem that evokes a sense of tranquility and appreciation for nature.'
]

new_instructions = instructions.generate_instructions(seed_examples,20)
```

### Generate Instances

```bash
seed_examples = [
{'input' : "Hello, how are you?",
'output' : "¡Hola, ¿cómo estás?"},
{'input' : "Can you please pass me the salt?",
'output' : "¿Puedes pasarme la sal, por favor?"},
{'input' : "I love going to the beach during summer.",
'output' : "Me encanta ir a la playa durante el verano."},
{'input' : "Where is the nearest post office?",
'output' : "¿Dónde está la oficina de correos más cercana?"},
{'input' : "What time does the movie start?",
'output' : "¿A qué hora comienza la película?"},
{'input' : "I need to make a reservation for two people.",
'output' : "Necesito hacer una reserva para dos personas."},
{'input' : "Could you recommend a good restaurant?",
'output' : "¿Podrías recomendarme un buen restaurante?"},
{'input' : "How do I get to the train station?",
'output' : "¿Cómo llego a la estación de tren?"},
{'input' : "What's your favorite book?",
'output' : "¿Cuál es tu libro favorito?"},
{'input' : "I want to learn Spanish.",
'output' : "Quiero aprender español."}
]

new_instances = instances.generate_instances(seed_examples,20,'Translate from English to Spanish')
```

### Transform DataFrame to List of Dictionaries

```bash
import pandas as pd

data = {
    'Input': [
        "Hello, how are you?",
        "Can you please pass me the salt?",
        "I love going to the beach during summer.",
        "Where is the nearest post office?",
        "What time does the movie start?",
        "I need to make a reservation for two people.",
        "Could you recommend a good restaurant?",
        "How do I get to the train station?",
        "What's your favorite book?",
        "I want to learn Spanish."
    ],
    'Output': [
        "¡Hola, ¿cómo estás?",
        "¿Puedes pasarme la sal, por favor?",
        "Me encanta ir a la playa durante el verano.",
        "¿Dónde está la oficina de correos más cercana?",
        "¿A qué hora comienza la película?",
        "Necesito hacer una reserva para dos personas.",
        "¿Podrías recomendarme un buen restaurante?",
        "¿Cómo llego a la estación de tren?",
        "¿Cuál es tu libro favorito?",
        "Quiero aprender español."
    ]
}

df = pd.DataFrame(data)

seed_examples = instances.transform_dataframe(df)
```
