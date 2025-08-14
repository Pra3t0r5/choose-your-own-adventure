from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.models import StoryLLMResponse, StoryNodeLLM
from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.utils import normalize_response_text

from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
    @classmethod
    # Underscored class methods are private methods by convention
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-5-mini")

    @classmethod
    def generate_story(cls, db: Session, session_id:str, theme: str = "fantasy") -> Story:
        # LLM Instancing
        llm = cls._get_llm()

        # Instancing the pydantic parser, specifying how we want the response to look like (StoryLLMResponse)
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                STORY_PROMPT
            ),
            (
                "human",
                f"Create the story with this theme: {theme}"
            )
        # Embeds the format_instructions as pydantic model on to STORY_PROMPT
        # and creates a prompt template with partially filled fields
        ]).partial(format_instructions=story_parser.get_format_instructions())

        # Generates and sends the prompt with no extra variables to fill "{}"
        raw_response = llm.invoke(prompt.invoke({}))
        response_text = normalize_response_text(raw_response)

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title, session_id=session_id)
        # Adding (marking as transient) allows us to keep using the class even after saving it to the db (marking as persistent) using flush
        db.add(story_db)
        db.flush()

        # lets get the root node
        root_node_data = story_structure.rootNode
        #if the root node is a dict
        if isinstance(root_node_data, dict):
            # gets check that the root node looks like we want
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        db.commit()

        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isEnding,
            iptions=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and (hasattr(node_data,"options") and node_data.options):
            options_list = []
            for options_data in node_data.options:
                next_node = options_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(db, story_id, next_node, False)

                # Creates mapping structure with a simplified version to avoid storing as a complexer tp access binary tree
                options_list.append({
                    "text": options_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()

        return node
