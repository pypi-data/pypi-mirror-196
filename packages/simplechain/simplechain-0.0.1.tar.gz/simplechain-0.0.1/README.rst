================
TODO
================
- [x] Try various options
    - Option 1: Train LLM on questions and answers of car fitments
        - Cons: Cannot handle new information (must be retrained)
        - Cons: May hallucinate answers
    - Option 2: Question driven framework
        - Description:
        - Cons: We must maintain dataset of car fitments
    - Option 3: Combined framework
        - Description: When a user says something:
        - The LLM generates a response.
        - Give products that fit the chat history
        - Ask questions that may narrow down the search

- [ ] All column values are indexed. Parts, makes, models, years,
- [ ] Keep track of what was asked to be verified and what was verified
- [ ] Add a testing framework using LLM's as testers
- [ ] Add unit testing for each module and integrations tests
- [ ] Add CI/CD before pushing to master
- [ ] Create a pipeline object to chain modules together (black box it)
- [ ] Add visualization
    - [ ] Add visualization for pipeline creation with injected resources
    - [ ] Inspect modules and resources during execution
    - [ ] Add a way to save and load pipelines
    - [ ] Compile the code to a single file
    - [ ] Sell as a service
- [ ] Add module caching with vector databases for nlp
- [ ] Add top level caching (caching the general state)

- Database schema
- Cost
- SQL cost

==============
How to build
==============
pip install -r requirements.txt

`python setup.py sdist bdist_wheel`

twine upload dist/*

twine upload --repository testpypi dist/*

pip install --index-url "https://test.pypi.org/simple/<package_name>"


================
Options
================
1. Single LLM entrypoint (questions, history, knowledge)
    1. Input -> LLM
        1. LLM -> Tool (Google search/SQL)
            1. Tool -> Google Search
            2. Tool -> SQL
            3. Tool -> QuestionRetriever
                1. QuestionRetriever -> LLM

2. Multi Entry entrypoint
    1. Did the user ask a question?
        1. If yes,

================
How to use
================

Resource
----------
Defines interfaces for resources that can be used by the pipeline.
.. code-block:: python

    @resource(name="TextGenerator")
    class LLMTextGenerator(ABC):
        @abstractmethod
        def complete(self, prompt: str) -> str:
            return True

    class OpenAITextGenerator(ABC):
        def __init__(self, api_key: str):
            openai.api_key = api_key

        def complete(self, prompt: str) -> str:
            return openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["\n", " Human:", " AI:"],
            )


Module
-----------
Transformers will transform the data in some way.
.. code-block:: python

    @module(name="LowerCase")
    def lowercase(input: str):
        return input.lower()

They can use resources:
.. code-block:: python

    @module(name="OpenAI")
    def openai(input: str, resource: OpenAITextGenerator):
        return resource.complete(input)

Control
---------
Control modules will redirect the flow of logic.

.. code-block:: python

    @control(name="hasFinalAnswer")
    def final_answer(input: str):

        if "Final Answer" in input:
            return 1
        else:
            return 2







