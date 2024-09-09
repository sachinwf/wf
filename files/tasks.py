from textwrap import dedent
from crewai import Task

class PreparationTasks():
	def extract_task(self,agent,bigstring):
		return Task(
			description=dedent(f"""\
				extract problem statement from {bigstring}"""),
			expected_output=dedent("""\
				string that is the problem statement"""),
			async_execution=True,
			agent=agent
		)



	def research_task(self, agent, idea):
		return Task(
			description=dedent(f"""\
				Conduct comprehensive research on the idea proposed
				Gather information on recent
				news, applications of the idea, historical development of the technology
				and relevant ideas already implemeneted by businesses.
				Idea proposed Context: {idea}"""),
			expected_output=dedent("""\
				A detailed report summarizing key findings about the idea application in the business world,
				case studies of implementation, and technology involved
				and companies involved in the space, highlighting implementation details that could be relevant for the final scope of work."""),
			async_execution=True,
			agent=agent
		)
	def tech_task(self, agent,idea):
		return Task(
			description=dedent(f"""\
				Conduct comprehensive technical deep dive on the idea proposed
				and what technology stack has been succesful in the past
				and how industry leaders have worked on creating product out of the idea
				Idea proposed Context: {idea}"""),
			expected_output=dedent("""\
				A detailed report summarizing key findings about the idea application in the business world,
				case studies of implementation, and technology involved
				and companies involved in the space, highlighting implementation details that could be relevant for the final scope of work."""),
			async_execution=True,
			agent=agent
		)

	def industry_analysis_task(self, agent, context):
		return Task(
			description=dedent(f"""\
				Analyze the current industry trends, challenges, and opportunities
				relevant to the meeting's context. Consider market reports, recent
				developments, and expert opinions to provide a comprehensive
				overview of the industry landscape.

				
				Meeting Context: {context}"""),
			expected_output=dedent("""\
				An insightful analysis that identifies major trends, potential
				challenges, and strategic opportunities."""),
			async_execution=True,
			agent=agent
		)

	def meeting_strategy_task(self, agent, context):
		return Task(
			description=dedent(f"""\
				Develop strategic talking points, questions, and discussion angles
				for the meeting based on the research and industry analysis conducted

				Meeting Context: {context}
				"""),
			expected_output=dedent("""\
				Complete report with a list of key talking points, strategic questions
				to ask to help achieve the meetings objective during the meeting."""),
			agent=agent
		)

	def summary_and_briefing_task(self, agent, context):
		return Task(
			description=dedent(f"""\
				Compile all the research findings, technical analysis, and industry analysis
				into a concise, comprehensive scope of work document for
				the management.
				Ensure the document has full details
				with all necessary information and implementation plan.

				Idea Context: {context}
				"""),
			expected_output=dedent("""\
				A well-structured scope of work document that includes sections for
				goals, objectives, deliverables, roles, responsibilities."""),
			agent=agent
		)

	def task5(self, agent, problem_statement):
		return Task(
			description=dedent(f"""\
				Write a detailed scope of work documentation that gives technology centered solution for:
    			{problem_statement}
    			
				A detailed scope of work document with well formatted sections take inspiration from government projects that
    have worked in the past across geographies. Give these as citations in the scope of work document.
    			"""),
			expected_output=("""A detailed scope of work document with well formatted sections take inspiration from government projects that
    have worked in the past across geographies. Give these as citations in the scope of work document.Create sections based on how other scope of work documents are built for similar problem statements.Do not include budget estimation section."""),
			agent=agent
		)

	def tasksection(self, agent, doc):
		return Task(
			description=dedent(f"""\
				With a section selected by the human of given {doc} please expand the section using the right tools and sources and cite these sources against those sections again
    			"""),
			expected_output=("""An edited version of the input document with the section expanded according to goal"""),
			agent=agent
		)




	def task6(self, agent, input_sow):
		return Task(
			description=dedent(f"""\
				Write a solution document that gives both high level and low level implementation plan given the scope of work document:
    			{input_sow}
				You should see how implementations from the citations in {input_sow} were done and draw inspiration.Make sure that the citations are correct.
				If possible draw a overview system architecture focusing on a high level modules and low level modules
    			"""),
			expected_output=("""A detailed solution document with well formatted sections like high level technology design, implementation plan,
    Use technical resources to draw system architecture diagram for each module needed to implement sultion at scale.
    Also give details on technology decisions, resources required and other sections you think a solution document should have.
    Make sure to elaborate each section so that it is self explanatory to someone who wants to implement this solution.
    Be very detail oriented in every section of the final document."""),
			agent=agent
		)





    


