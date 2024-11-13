import os

from crewai import Crew, Process

from langflow.base.agents.crewai.crew import BaseCrewComponent
from langflow.io import HandleInput, SecretStrInput


class HierarchicalCrewComponent(BaseCrewComponent):
    display_name: str = "Hierarchical Crew"
    description: str = (
        "Represents a group of agents, defining how they should collaborate and the tasks they should perform."
    )
    documentation: str = "https://docs.crewai.com/how-to/Hierarchical/"
    icon = "CrewAI"

    inputs = [
        *BaseCrewComponent._base_inputs,
        HandleInput(name="agents", display_name="Agents", input_types=["Agent"], is_list=True),
        HandleInput(name="tasks", display_name="Tasks", input_types=["HierarchicalTask"], is_list=True),
        HandleInput(name="manager_llm", display_name="Manager LLM", input_types=["LanguageModel"], required=False),
        HandleInput(name="manager_agent", display_name="Manager Agent", input_types=["Agent"], required=False),
        SecretStrInput(
            name="openai_api_key",
            display_name="OpenAI API Key",
            info="The OpenAI API Key to use for the OpenAI model.",
            value="OPENAI_API_KEY",
        ),
    ]

    def build_crew(self) -> Crew:
        tasks, agents = self.get_tasks_and_agents()

        # Set the OpenAI API Key
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.hierarchical,
            verbose=self.verbose,
            memory=self.memory,
            cache=self.use_cache,
            max_rpm=self.max_rpm,
            share_crew=self.share_crew,
            function_calling_llm=self.function_calling_llm,
            manager_agent=self.manager_agent,
            manager_llm=self.manager_llm,
            step_callback=self.get_step_callback(),
            task_callback=self.get_task_callback(),
        )
