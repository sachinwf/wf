from textwrap import dedent
from crewai import Agent

# from tools.ExaSearchTool import ExaSearchTool
import streamlit as st
import os
from crewai_tools.tools import WebsiteSearchTool
os.environ['OPEAI_API_KEY'] = st.secrets["openai_api_key"]


web_search_tool = WebsiteSearchTool()




class PreparationAgents():
	def string_to_problemstatement(self):
		return Agent(
			role='simple extractor',
			goal='get problem statement from a big string',
			tools=[web_search_tool],
			backstory=dedent("""\
					simple extractor"""),
			verbose=True
		)

	def research_agent(self):
		return Agent(
			role='Research Specialist',
			goal='Conduct thorough research on people and companies involved in the meeting',
			tools=[web_search_tool],
			backstory=dedent("""\
					As a Research Specialist, your mission is to uncover detailed information
					about the sectins and entities . Your insights
					will lay the groundwork for strategic document preparation."""),
			verbose=True
		)
	def technology_agent(self):
		return Agent(
			role='Technology Research Specialist',
			goal='Based on the idea proposed,you select specific technology stacks and pieces that will help create final product',
			tools=[web_search_tool],
			backstory=dedent("""\
					As a technology Specialist, you share technology specifics that are needed to take idea to product,
					which includes tech stacks and past technology used in creating the same idea,this includes 
					research done by technology thought leaders, case studies and low level implementation details."""),
			verbose=True
			)

	def industry_analysis_agent(self):
		return Agent(
			role='Industry Analyst',
			goal='Analyze the idea on basis of current industry trends, challenges, and opportunities',
			tools=[web_search_tool],
			backstory=dedent("""\
					As an Industry Analyst, your analysis will identify key trends,
					challenges facing the industry, and potential opportunities that
					could be leveraged to make the idea proposed a success."""),
			verbose=True
		)

	def meeting_strategy_agent(self):
		return Agent(
			role='Meeting Strategy Advisor',
			goal='Develop talking points, questions, and strategic angles for the idea proposed',
			tools=[web_search_tool],
			backstory=dedent("""\
					As a Strategy Advisor, your expertise will guide the development of
					talking points, insightful questions, and strategic angles
					to ensure the idea's objectives are achieved."""),
			verbose=True
		)

	def summary_and_briefing_agent(self):
		return Agent(
			role='Scope of work writer',
			goal='Compile all gathered information into a scope of work document',
			tools=[web_search_tool],
			backstory=dedent("""\
					As the scope of work writer, your role is to consolidate the research,
					analysis, and strategic insights into goals, objectives, deliverables, roles, responsibilities for the idea"""),
			verbose=True
		)
######
#.	Project Management Professional (PMP)
#2.	Certified ScrumMaster (CSM)
#3.	PRINCE2 Practitioner
#4.	Certified Lean Six Sigma Green Belt
#5.	Certified Lean Six Sigma Master Black Belt
#6.	Certified Associate in Project Management (CAPM)
#7.	Certified in Production and Inventory Management (CPIM)
#8.	Certified Business Analysis Professional (CBAP)
#9.	Agile Certified Practitioner (PMI-ACP)
####

	def scopeofwork(self,role_name):
		return Agent(
			#role='provide best technology based solution based on problem statement',
			role=str(role_name),
			goal='Given the problem statement provide a scope of work document using your expertise and training based on role',
			tools=[web_search_tool],
			backstory=dedent("""\
					you are an expert Lean Six Sigma Master Black Belt Expert consultant that helps in giving advisory on technology solutions to problems in governments.Double check the citations that are suggested in the task."""),
			verbose=True
			)

	# def citation_check(self):
	# 	return Agent(
	# 		role='given the citation links given in scope of work document,check if link works and replace with working link',
	# 		goal='Edit document to have corect citations link',
	# 		tools=[web_search_tool],
	# 		backstory=dedent("""\
	# 				Citation link checcking."""),
	# 		verbose=True
	# 		)

	def expand_section(self):
		return Agent(
			role='provide more relevant details to a particular section of a document',
			goal='provide clear overview of how the section will be expanded and after human confirmation add to document.',
			tools=[web_search_tool],
			backstory=dedent("""\
					you are an expert technology consultant that goes deeper into particular subsections selected by governemtn offical."""),
			verbose=True,
			human_input=True
			)



	def create_solutiondoc(self,role_name):
		return Agent(
			role=str(role_name),
			goal='provide a clear high level and low level details on technology implementation with focus on expanding each section.',
			tools=[web_search_tool],
			backstory=dedent("""\
					you are an expert based on the role that takes a scope of work document to detailed solution document for government projects."""),
			verbose=True
			)






