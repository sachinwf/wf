from dotenv import load_dotenv
load_dotenv()
import sys
from crewai import Crew
import os
from files.tasks import PreparationTasks
from files.agents import PreparationAgents
import streamlit as st

import time
tasks = PreparationTasks()
agents = PreparationAgents()
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])
import os
#prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{input}")])
task_values = []
#display the console processing on streamlit UI
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

       

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []



if "chat_history" not in st.session_state:
	st.session_state['chat_history'] = []



def get_completion1(prompt, model="gpt-4o-mini", temperature=0): 
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,response_format={ "type": "json_object" },
    messages=messages,
    temperature=temperature)
    return response.choices[0].message.content

def extract_ps(text):
    prompt = f""" please respond with json and
extract the problem statement from the. \ 
```{text}```
"""
    response = get_completion1(prompt)
    #print(response)
    return response



import re


def extract_problem_statement(text):
    # Define a regex pattern to match the problem statement
    # This example assumes the problem statement starts with "Problem:" or similar keywords
    pattern = r'\{.*?"ProblemStatement"\s*:\s*"(.*?)"\s*\}'

    # Search for the pattern in the text
    match = re.search(pattern, text, re.IGNORECASE)
    #print(match.match)
    # If a match is found, return the extracted problem statement
    if match:
        return match.group(1).strip()
    else:
        return "Problem statement not found."

#if([0:2]=="AI"):



        


# Initialize the session state
if 'selection' not in st.session_state:
    st.session_state['selection'] = 0

if 'sow_result' not in st.session_state:
    st.session_state['sow_result'] = []

selected = st.selectbox('Choose what type of expert you want to work on the SOW doc:', ('None','Certified Lean Six Sigma Master Black Belt', 'PRINCE2 Practitioner'), index=st.session_state['selection'])

if(st.session_state.chat_history != ""):
	last_response = str(st.session_state.chat_history[-1])
	#print(last_response)


	if("problem_statement" in last_response):
		ps = extract_ps(str(st.session_state.chat_history[-1]))
		




		if(ps):
			if selected != 'None':
				scopeofwork = agents.scopeofwork(selected)
				#create_solutiondoc = agents.create_solutiondoc()
				taskx = tasks.task5(scopeofwork,ps)
				# #tasks_section = tasks.tasksection(scopeofwork,)

				# Create Crew responsible for Copy
				crew = Crew(
						agents=[
							#researcher_agent,
							#technology_agent,
							#industry_analyst_agent,
							#summary_and_briefing_agent
							scopeofwork
							#citation_check
						],
						tasks=[
							taskx
							#citation_check_task
							#research,
							#tech,
							#industry_analysis,
							#summary_and_briefing

						]
					)
				crew_result = crew.kickoff()
					#game = crew.kickoff()
					# Placeholder for stopwatch
				stopwatch_placeholder = st.empty()
			        
				# Start the stopwatch
				start_time = time.time()
				with st.expander("Processing!"):
				    sys.stdout = StreamToExpander(st)
				    with st.spinner("Generating Results"):
				    	#print(st.session_state['sow_result'])
				    	st.session_state['sow_result'].append(crew_result)
				        


				# Stop the stopwatch
				end_time = time.time()
				total_time = end_time - start_time
				stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")

				#st.header("Tasks:")
				#st.table({"Tasks" : task_values})

				st.header("Results:")
				st.markdown(crew_result)
				st.session_state['sow_result'].append(crew_result)
				#print(st.session_state['sow_result'])
				
				


			# # Print results
			# print("\n\n################################################")
			# print("## Here is the result")
			# print("################################################\n")
			# print(game)

			# taskx1 = tasks.task6(create_solutiondoc,game)


			# crew2 = Crew(
			# 	agents=[
			# 		#researcher_agent,
			# 		#technology_agent,
			# 		#industry_analyst_agent,
			# 		#summary_and_briefing_agent
			# 		create_solutiondoc
			# 	],
			# 	tasks=[
			# 		taskx1
			# 		#research,
			# 		#tech,
			# 		#industry_analysis,
			# 		#summary_and_briefing

			# 	]
			# )



			# #taskx1 = tasks.task_scopeofwork(create_solutiondoc,game)

			# game2 = crew2.kickoff()

			# print(game2)





	# problem_statement2="""
	# The central government of Bulgaria has multiple citizen benefiaciary schemes, but the citizens have no way to know about them.
	# Access to citizen phone numbers does not exist. Billions in goverment aid is lost every year.
	# """
	# problem_statement4 = """
	# "How to efficiently provide credit to farmers who often lack the necessary documentation, while ensuring the process is transparent and fair for all stakeholders including scheme owners and banks?"
	# """

	# problem_statementxxx = """
	# "The Ministry of Education seeks to effectively integrate digital technology into colleges across various disciplines including medical, engineering, law, and humanities in India. The goal is to establish digital classrooms that will benefit both students and faculty. Currently, these institutions rely heavily on traditional pen-and-paper methods with no significant use of technology in the learning process. There is a need to collect and utilize relevant data to facilitate this transition and measure its impact."
	# """

	# print("## Welcome to the idea  Prep Crew")
	# print('-------------------------------')
	# # idea = input("What idea do you want me to make a scope of work document for?\n")
	# # context = input("What is the context of the idea that needs to be implemented?\n")
	# # #objective = input("What is your objective for this meeting?\n")

	# # # Create Agents
	# # researcher_agent = agents.research_agent()
	# # technology_agent = agents.technology_agent()
	# # industry_analyst_agent = agents.industry_analysis_agent()
	# # meeting_strategy_agent = agents.meeting_strategy_agent()
	# # summary_and_briefing_agent = agents.summary_and_briefing_agent()



	# #######create agents
	# #technology_agent = agents.technology_agent()


	# # Create Tasks
	# ##research = tasks.research_task(researcher_agent, idea)
	# #tech = tasks.tech_task(technology_agent,idea)
	# #industry_analysis = tasks.industry_analysis_task(industry_analyst_agent, context)
	# #meeting_strategy = tasks.meeting_strategy_task(meeting_strategy_agent, context)
	# #summary_and_briefing = tasks.summary_and_briefing_task(summary_and_briefing_agent, context)

	# #meeting_strategy.context = [industry_analysis]
	# #summary_and_briefing.context = [industry_analysis, meeting_strategy]