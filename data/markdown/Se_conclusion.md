# Software Project Management

Lesson Objectives:
- What is Project Management
- Techniques for sw cost estimation
- Measuring the size of a sw project
- Lines of code
- Function Point
- Algorithmic Estimation
- COCOMO

# Brooks' Law

_Adding personnel to a late sw project will delay it even more_
by F. Brooks, _The mythical Man-Month_ , 1975

# Some definitions:
- **Project** : temporary undertaking undertaken to achieve a goal
- **Project Management** : application of knowledge, techniques and tools to the activities of a specific project in order to bring it to a successful conclusion.
- **Product Management** : business function of planning, manufacturing and marketing a specific product that follows a product life cycle.

Variables that govern a project:
- Scope: user requirements, quality specifications, deliverables
- Cost: budget and resources needed
- Time: start, end and schedule of activities

A project is considered successful if it finishes on time, within budget, and delivers what the user expects.

# The project management triangle

For every project the three constraints: scope, resources, and time are related.
- Increasing the scope and fixing it (functions + quality) means increasing the project time and costs;
- Reducing the time requires higher costs (more resources) or a narrower scope;
- A tight budget (fewer resources) can imply longer times or a reduction in the scope.

The scope is usually more important than the other two constraints: in planned models it is the independent variable. In agile models instead the independent variables are duration and costs, the scope and quality are negotiated.

# The Project Manager (PM)

- The Project Manager (PM, or project manager) controls the project planning and budget.
- Throughout the life cycle the PM must control **costs** and **resources** of a project:
- **Initially** to verify the feasibility of the project
- **During the project** to check that resources are not wasted and budgets are respected
- **At the end** to compare the budget and the actual

Tasks of the PM:
1. Understand the project objective
2. Identify the development process
3. Determine the structure of the project team
4. Identify the management process
5. Develop a team activity calendar
6. Plan the acquisition of people in the team
7. Begin risk management
8. Identify the documents to be produced
9. Begin the process...

# Agile teams do not have a PM
- Why do agile teams NOT have a Project Manager?
- In the Agile philosophy, the role and responsibilities traditionally attributed to the “ **project manager** ” are distributed across multiple roles.
- Example: in the agile Scrum model the roles that have PM responsibilities are **Product Owner** and **Development Team** (the Scrum Master is a facilitator, process owner but not responsible for management).

Project Management - Body of Knowledge (PMBOK)

- The PMBOK manual is a PMI publication that describes the notions and methods needed by PMs “in most projects”
- It is updated periodically (most recent edition: 2021)
- It structures Project Management by defining nine areas of expertise
- IEEE 1490-2011 is “Guide adoption of PMI standard to the project management BoK”

# Project time management
- Definition of activities
- Sequencing of activities
- Estimating resources for activities
- Estimating duration of activities
- Scheduling of activities
- Controlling activities

# Terminology
- Work breakdown: articulation (i.e. list and relationships) of project activities
- Milestone: significant event in the life of a project
- Critical path: sequence of activities whose duration is incompressible

### Work Breakdown Structure (WBS)
### Gantt Chart
### Taiga

# Estimating and measuring a sw project
- Design of the software can be analyzed by studying five variables: cost, duration, effort, productivity and number of errors in the sw product [Putnam 1992].
- The project manager has two important tasks with respect to these variables: to estimate them in advance, to measure them during the project, and to report them in the final report.
- How can we estimate cost, duration, effort, productivity and number of errors before the project begins?

### The cone of uncertainty in sw development.
### Uncertainty in sizing

# Value and cost of the sw

The _value_ of a sw is proportional to the number of users.
Value (sw) = #users*average revenue per user
The _cost_ of a software is proportional to the development effort (in months/person), which in turn is proportional to the size ( _size_ ) of the sw.

**Productivity**

- Productivity is an economic abstraction that is calculated with the output/input ratio
- The _productivity_ of a team that has produced a software of size size with a given effort is
calculated size(sw)/effort
- Example: « _the team had a productivity of 5K LOC/person-month_ »

# Technical debt

Technical debt is an estimate of the cost of future additional effort caused by a premature solution adopted today in order to deliver a product with some value (the future effort will have to be repaid with interest).

In good quality software, the following inequality should apply to each _version_:
Value ( _version_ ) >> Cost ( _version_ ) + Technical Debt ( _version_ )

**Development Cost Estimation Techniques**

The main techniques for estimating project costs:

- **top-down** (or analog): use of the cost of a similar project or with known cost components as the basis for estimating the new project
- **bottom-up** : estimate of the individual tasks that make up the project and add them together to obtain the total estimate
- **Design-to-cost** : use of experts to determine how much functionality can be produced with the available budget
- **parametric** : estimate based on the use of a mathematical model that uses a grid of parameters

# What should be estimated

- **Duration** : time span of the project, from start to finish; depends on the dependencies between project activities; usually measured in months
- **Effort** : sum of the times of all project activities; usually measured in months/person (mp)
- **Team size** is obtained from the effort/duration relationship

Example:
- A project must last one year, involving four people, two of whom are half-time
- Duration is 12 months
- Effort is 36 months/person

Do not confuse duration and effort!

Example:

- The legal _duration_ of a degree course is three years
- The _effort_ is 180 credits (established by law)
- One credit is equal to 25 hours/student

**Note 1** : The Degree Course Regulations could define different durations (e.g. six years), while maintaining the effort of 180 credits required by law.
**Note 2** : the cfu (=25h/student) is a unit of measurement of the effort (different from the month/person, which is not defined univocally, but for example in COCOMO is equal to 152 h/person).

# The components of the cost of the Sw

The main components of sw cost are:
- Cost of the development hardware
- Cost of the development software
- Cost of human resources ( **effort** )
- Overall **Duration**

Planning begins with the estimate of the size of the software.

# Measuring project size

- The **_size_** of a software project is the first cost factor in many models that estimate duration and effort
- There are three measures that estimate the size of a software to be produced:
- Lines of code
- Function points
- History points in agile processes
- These measures need historical data to be “calibrated” with respect to the organization that uses them.

# Lines of code (LOC)

- The most common measure of the size of a software project is the number of lines of source code ( Lines of Code , LoC; 1 KLoC = one thousand lines of source code).
- LoC can take into account empty lines or comments (CLoC); in general we have: LoC = NCLoC + CLoC, ​​that is, comments are counted
- The most common distinction is between physical LoCs and logical LoCs

Physical and logical LoCs are different.

LOC: pros and cons

- Derived metrics:
- $ per KLOC
- errors or defects per KLOC
- LOC per person-month
- documentation pages per KLOC
- Errors per person-month
- $/documentation page
- Source code is the tangible product of the development process, and there is already a lot of literature on its LOC measurement.
- However, the LOC measurement depends on the programming language.
- Furthermore, it penalizes (underestimates productivity) well-written and concise programs.

# Critical aspects of size estimates

1. It is difficult to estimate the size in LOC of a new application
2. The LOC estimate does not take into account the different complexity and power of the instructions (of the same language or different languages)
3. It is difficult to define precisely the counting criterion (instructions split on multiple lines, more instructions on a line...)
4. Could a higher productivity in LOC lead to more bad quality code?
5. Should undelivered code (e.g. tests) be counted?

# Function Point [Albrecht] 
Function Point analysis enumerates the functionality of a system from the user point of view.

“ _The original objective of the Function Points work was to define a measure [that would] help managers analyze application development and maintenance work and highlight productivity improvement opportunities._ ” “ _The Function Points method measures the equivalent functions of end-user applications regardless of the language, technology, or development environment used to create the application._ ” # Example: plant information system Calculation of FP (Function Point): step 1 The application to be created is described.
We start from a **description** of the system (**specification**) of a functional nature.

Calculating FP: Step 2
Find the following elements in the **user requirements description**:
- External Input: information, data provided by the user (e.g. file name, menu choices, input fields)
- External Output: information, data provided to the application user (e.g. reports, error messages)
- External Inquiry: interactive sequences of requests – responses
- External Interface File: interfaces with other external information systems
- Internal Logical File: main logical files managed in the system

FP calculation: step 3

The individual functional elements must be classified by design complexity, using the following weight table.

Calculating FP: step 4
List the elements of each type, multiply by their “weight” and add:
UFC= Σ (^) [i=1_5] (Σ (^) [j=1_3] ( element i,j * weight i,j))
Where i = element type
j = complexity (simple or medium or complex)
UFC = Unajdjusted Function Count

FP calculation: step 5

Define the application technical complexity factor (TFC).

TFC calculation:

**TFC = 0.65+0.01* Σ** (^) **[i =1-14] Fi**

Each Fi factor is evaluated between 0 (irrelevant) and 5 (maximum).
The overall TFC value varies in the range from 0. 65 (easy development) to 1. 35 (difficult development).

FP calculation: final step
The formula is finally:
FP = UFC * TFC

# Summary of the method

Requirements of a product or software system.
Analysis using FP counting rules.
External inputs, External interfaces, Dialogs, Internal logic files, Outputs external.
FP Counting.

Example:

- Internal logical files
    - Customer DB
    - Current accounts DB
    - Payments DB
    - Banks DB
- External interface files
    - Customer management manager GUI
    - Sales manager GUI
    - External inputs
    - Account creation
    - Account deletion
    - Card recharge - Card balance
    - Request payment amount
- External queries
    - View customer status
    - View payment status
    - View balances
- External inputs
    - Payment notification
    - Management of card sending

# Calibration

- The FP counting is based on subjective judgments, so different people can achieve results different.
- When introducing FP Analysis (abbreviated as FPA) in an organization, a calibration phase is necessary, using the projects developed in the past as the basis of the counting system.

# Cost per FP

Some developers use cost scales based on FP for contracts.
- Initial requirements = $500 per FP;
- Changes in the first three months = $600 per FP;
- Subsequent changes = $1000 per FP

Cost Model-Based Estimating
- Cost models allow for a “quick” estimate of effort, useful during the very early stages of a project
- This first estimate is then refined, later in the life cycle, by means of factors called **cost drivers**
- The calculation is based on the **effort equation** :
- **E = A + B*SC** where E is the effort (in person-months), A , B, C are parameters dependent on the project and the organization that executes it, S is the size of the product estimated in KLOC or FP.

# Software Cost Problems

Software costs are dominant, as a percentage of total information systems costs .

Software cost estimation problems are caused by:
- failure to accurately size a project;
- failure to define the overall process and operating environment of a project;
- inadequate assessment of personnel, in quantity and quality;
- lack of quality requirements for estimating specific activities within the project

# Software Cost Models

Examples of business models:
- COCOMO
- COSYSMO
- COSTXPERT
- SLIM
- SEER
- Costar, REVIC, etc.

Use of parameters for estimates

Size of the system to be produced * Project attributes = Estimates:
- Effort
- Costs
- Duration
- Deliveries

# Software cost models: COCOMO

- Barry Boehm's **Constructive Cost Model** ( **COCOMO** ) is one of the most popular parametric models for estimating software projects.
- COCOMO 1 is described in the book _Software Engineering Economics_ , 1981
- COCOMO 2 is described in the book _Software Cost Estimation_ , 2000
- COCOMO is a regression-based model (i.e., a historical archive) that considers various parameters of the product and the organization that produces it, weighted by an evaluation grid

COCOMO: equational form

- The main calculation of COCOMO is based on the Effort Equation to estimate the number of person-months mp needed for a project.
Estimated_Cost = # mp * labor_cost
- Most of the other estimated quantities (duration, staff size, etc.) are then derived from this equation.
Where:
- **Performance** = Effort
- **Complexity** = Size of generated code
- **Process** = Maturity of the process and method
- **Team** = Skills, experience, motivation
- **Tools** = Process automation

Performance = ( Complexity ) ^(Process) * ( Team ) * ( Tools )

# COCOMO 1
- Boehm built the first version of a cost model called CoCoMo 1 in 1981
- CoCoMo 1 is a collection of three models:
- **Basic** (applied at the beginning of the project life cycle)
- **Intermediate** (applied after the requirements specification)
- **Advance** (applied at the end of the design phase)

- The three models have equational form:
**Effort = a*Sb*EAF**

- Effort is the effort in person-months
- EAF is the _settling coefficient_
- S is the estimated size of the source code to be delivered, measured in thousands of lines of code (KLOC)
- a and b are coefficients that depend on the type of project

Types of projects in COCOMO1:
- **Organic mode** (simple project, developed in a small team)
- **Semidetached mode** (intermediate difficulty project)
- **Embedded** (project with very constraining requirements and in an unknown field)

# Intermediate Model

- Takes the basic model as a reference
- Identifies a set of attributes that influence the cost (called _cost driver_ )
- Multiplies the basic cost by a factor that can increase or decrease it
- The estimate of this model gets the real values ​​right with an approximation of ±20% about 68% of the time
- (Most used model with COCOMO 1)

Calculation of the multiplication factor:
- The multiplication factors due to the attributes each have a value that indicates the shift from the normal value of that specific attribute.
- The value of the different factors is determined by taking into account past projects (calibration).
- The product of the evaluation of the relevant attributes forms EAF.

Project Management in SWEBOK

# Self-test questions

- What are the tasks of a project manager?
- What is the cone of uncertainty?
- What is a person-month? How many person-hours is it worth?
- Does the process influence the cost of software development?
- What is a line of code? What is a function point?
- Does a programmer prefer to be paid per LOC or per FP achieved?
- What does the COCOMO model calculate?
- What is a history point?

# Software quality
Lesson objectives:
- The risks of poor software quality
- Quality standards
- Testing

Software Engineering Disaster Hall of Fame.

# Guiding principles of software development

- Develop iteratively
- Use component architectures
- Manage requirements
- Model graphically
- Verify quality
- Control changes

What is software quality? Some possible answers:
- No defects!
- Good performance!
- Both on Mac and PC!
- Easy to use
- Suitable for my needs!
- I want to use it for a long time!
- It must be cheap!

# Errors, defects and failures

The “life” of a bug:
- The programmer makes a mistake while writing a line of code;
- The error can have several negative effects: it becomes a defect ( _fault_ )
- The defect directly causes an exception/unwanted output: it becomes a failure

From IEEE Standard Glossary of SE Terminology

- **Error** : cause of a defect;
example: a human error in interpreting the specification or in using a method
- **Fault** : source defect ( _bug_ ), causing a failure
- **Failure** : behavior of the sw not foreseen by its specification

Standard classification of software problems.

# Why is the sw defective?

- Humans make mistakes, especially when performing complex tasks; this is inevitable
- Experienced programmers make an average of one error every 10 lines
- About 50% of coding errors are caught at compile time
- Other errors are caught by testing
- About 15% of errors are still in the system when it is delivered to the customer

**Failures vs. Defects**

- MTTF: mean time to failure
- defects are more dangerous the more frequent the failures that result from them
- The figure shows that you have to look for the most common defects that cause the most frequent failures,
- These “common” defects are few compared to the total failures: many are rare or very rare
- So eliminating defects does not necessarily improve the quality of a software system!

# Objectives of this lesson
- Defining quality
- Defining the qualities of processes and software products
- Internal qualities - visible to the designer
- External qualities - visible to the user
- How to evaluate quality
- Measuring quality indicators
- The Goal-Question-Metric (GQM) method
- Verifying quality: testing techniques
Discussion:
- How can we say that a software product is of good quality (rating)?
- How can we say that a software product is better than another (ranking)?

# Quality of software products

**1. The product must meet its specification**
- Tests that verify the code against the requirements are the foundation on which to measure quality
**2. The product must not contain defects**
- But it is very difficult to produce error-free software
**3. The product must comply with industry standards**
- Which international standards define the quality criteria to evaluate the product and its development process?
**4. The product must have the characteristics that are expected from a professional implementation**
- For example, the maintenance cost of a software product must be low and correspond to the customer's expectations

# Tests guarantee quality

_Any code "delivered" without its tests is poorly done._

_It does not matter if it is well written; it does not matter if it is object-oriented or well formatted._

_If we have tests, we can modify the behavior of the code quickly and in a controllable way._

_Without tests, we do not really know if our code gets worse or better._

# Software quality

- Functional quality: degree of satisfaction of functional requirements, assessed by verification ( testing ).
- Structural quality: degree of satisfaction of non-functional requirements, assessed by validation.

Product quality attributes

- Related to operational characteristics
- Correctness (does it meet its functional specification?)
- Reliability (correctness over time)
- Efficiency (does it waste resources?)
- Integrity (does it damage data or resources?)
- Resilience (ability to recover from abnormal situations)
- Related to the ability to undergo changes
- Readability and testability
- Maintainability
- Related to adaptability to new environments
- Portability
- Reusability
- Interoperability
- Usability (how usable is it with different users and in different contexts?)

Tom DeMarco's principle: You can't control what you can't measure!

# Measure the qualities of the sw.

Software quality is measured in many ways:
- process quality
- internal quality attributes
- external quality attributes
- quality in use attributes

In any software life cycle the **measurable** entities are:
- resources used (time, effort)
- some process attributes (e.g. productivity)
- some product attributes (e.g. defects)

How important is it to measure?

Reasons for Software Lawsuits:
- Unstable, constantly changing requirements 95%
- Inadequate quality control, no measurements 90%
- Poor monitoring of the development process 85%
- Incorrect cost or time estimates 80%
- False promises by vendors 80%
- Optimistic or arbitrary estimates 75%
- Informal, unstructured development 70%
- Inexperienced customers unable to define their requirements 60%
- Inexperienced project managers 50%
- Failure to use static analysis techniques or inspections 45%
- Reuse of buggy software 30%
- Inexperienced or unqualified engineering team 20%

# Who cares about SW measurements

- Individual developers – Distribution of effort: Who cares about SW measurements
- Estimated and actual duration and effort
- Code covered by unit testing
- Number of defects found from unit testing
- Complexity of the project and code
- Project team
- Product size
- Distribution of effort
- Requirements status (#approved, #implemented, #verified)
- % of test cases passed
- Estimated and actual duration between two major milestones
- Estimated and actual staffing levels
- #defects found by integration and system tests
- #defects found by inspections
- Defect status
- Requirements stability (#requirements changed during development)
- Number of tasks planned and completed
- Organization developing software
- Levels of defects released ( _critical_ , _major_ , _average_ , _minor_, _exception_ )
- Product development cycle time
- Accuracy of estimated planning and effort
- Actual reuse
- Estimated and actual cost

# Measuring software product quality

The quality of a software product is the measure in which the product meets its specification.
Internal and external quality attributes:
- external attributes: visible to the user
- internal attributes: visible to manufacturers

How to introduce quality:
- Any quality assessment starts from the _purpose_ of the person who wants to evaluate it
- Those who evaluate the quality of a product or process should:
- have clear objectives,
- link them to specific questions about the products or processes being analyzed, and
- define metrics capable of analyzing and quantifying the qualities required of the products with respect to the objectives

# Goal Question Metric (GQM)

- Method for defining software metrics
- Developed to evaluate software defects in NASA projects, and then generalized

- Steps:
- Understand and analyze the objectives of the project or organization
- For each objective, define the questions that need to be answered in order to understand whether the objectives have been achieved or not
- Establish which attributes need to be measured in order to answer the questions

The **Goal-Question-Metric** (GQM) method is used to define project, process and software product measures so that:
- Measurement is simple
- Measurement data can be used in a constructive and shared way
- Metrics and their interpretation reflect the values ​​and views of different stakeholders

GQM is based on three levels:
- Conceptual level (goal): A goal for an object of study is defined with respect to various quality models and from various points of view, relative to a particular environment.
- Operational level (question): A set of questions is used to define models of the object of study to assess the required goal.
- Quantitative level (metrics): A set of model-based metrics is associated with each question in order to characterize the answers in a measurable way.

GQM: Modeling Hierarchy
- First the goals (conceptual phase)
- Then the questions (operational phase)
- Finally the metrics (quantitative phase)

# Using GQM (Goal-Question-Metric):
- GQM can be used in all phases of software development
- It can be applied to projects, processes and products
- The metrics that are defined must relate to the objectives of the organization
- Measurements should be useful and constructive, because
the organization must learn by analyzing them
- Metrics and their definitions should reflect the point of view of
different stakeholders (e.g. developers, users, designers, etc.)

Planning a quality model with GQM
1. Developing goals and associated quality measures
2. Generating questions that define the goals, quantifying them
3. Specifying the measures to be collected in accordance with the goals
4. Developing operational mechanisms for collecting the measures
5. Collecting data and analyzing them to develop corrective actions
6. Analyzing Postmortem Data for Future Recommendations

# What is “quality”?

Problematic points for a software system

- Quality is not just the absence of defects in the final product
- Often, requirements for external qualities (e.g. efficiency, reliability) and those for internal qualities (e.g. maintainability, reusability) are antithetical, and must be balanced
- Some quality requirements are difficult to specify
- Specifications are often **incomplete** and sometimes **inconsistent** , but we cannot wait for specifications to improve before worrying about the quality of the final product.

Objectives of Verification and Validation

- **Verification** :
_Comparison of a product with its specification_ (i.e., comparison of a product with its requirements)
- **Validation** :
_Acceptance of the product by the customer_

**Note** : According to some, “verification” determines whether a certain activity has been performed correctly, while “validation” certifies that a product meets its requirements; we do NOT use these terms.

# Software development activities

- Requirements gathering (use case model)
- Requirements analysis (domain objects)
- System Design (subsystems)
- Object design (system objects)
- Implementation (source)
- Testing (test cases)

# Verifications

- The _verification_ activity, as well as the _documentation_ activity, is not a separate phase of the process
- However, it is advisable that it is carried out by people other than those involved in design or coding
- Each document produced should be checked (possibly by people other than the authors of the document) and systematically documented itself
- There are two types of verification: the one based on analysis (inspection) and the one based on execution (testing)

Development activities related to quality:
- **Testing** : process of investigating the risks associated with the execution of a software system
- **Measurement** : of quality indicators, both through inspection and execution
- **Verification** : analysis of functions with respect to the specification
- **Validation** : acceptance by stakeholders
- **Certification** : analysis of functions with respect to the legal requirements to be certified

# Testing
- Testing of a software product is a process activity that has the purpose of measuring the risks associated with the use of a software product in execution.
- The artifacts produced by testing are the test plans that include the test cases, the test suites that automate the testing, and the test reports that contain the results of the activity.

Phases/Types of Testing
- **Unit testing**
- Testing of individual components
- **Module testing**
- Testing of collections of related components
- **Sub-system testing**
- Testing of integrated modules: attention to interfaces
- **System testing**
- Testing of the entire system. Testing of “emergent” properties (not attributable to individual components)
- **Acceptance testing**
- Testing with customer data (and presence) to check that the system behavior is acceptable

Types of Testing:
Unit
Module
Component
Subsystem
Integration
System
Acceptance

# Testing Artifacts

Test plan artifact that details specific testing objectives, resources, and processes for a software product.
Test design artifact that guides the implementation of tests.
Test case set of conditions or variables under which a tester determines whether a software application or system responds correctly or not.
Test procedure formal specification of test cases to be applied to a product.
Test item transmittalreport artifact that identifies the status and metadata of test elements.
Test log recording of the results of a test, with the result: passed or failed.
Test incident When the result of the test is unexpected, then it is called an incident (can be an error, a defect, a problem).
Test summary Summary of the results of a test.

Requirements and tests:
- Testing is intended to verify that the code meets the requirements.

Testing is difficult:
- Requirements are not always clear
- Many developers do not know testing techniques or tools
- Testing is considered “boring” or “expensive”
- Often there is no time to test “everything” well

**Note** : Systematic and exhaustive testing is computationally intractable; however, we must make every effort to eliminate every possible defect or risk factor.

# Define a test plan

- Comprehensive (but not excessive)
- Use a test matrix
- Include positive and negative tests
- Find “interesting” test cases
- Run each test at least twice
- Update the plan during development
- Add regression tests
- Take advantage of user feedback
- Guard against product and test obsolescence

Types of tests:
- Unit or module
- Individual classes or types
- Component
- Group of related classes
- Integration
- Interaction between components

Design tests:
- Tests are “attacks” on the software conducted to see if there are defects or risks
- Test methods
- Direct
- Indirect
- Look for and hit vulnerabilities
- Black box
- White box

Direct testing:
- Usually automatic
- Low level
- Only basic functionality
- Leverages specifications

Indirect testing:
- Usually manual
- High level
- Scenarios “realistic”
- Discovers many unexpected errors

# Testing a module

- **Black-box testing** (functional, data-driven, I/O-driven): test cases are defined in the specification document; product code is ignored during testing.
- **White-box testing** (glass-box, logic-driven, path-oriented): test cases are defined on the source code.
- Note: _Testing exhaustively (i.e. in all possible cases) is impossible_
**Example (I/O-driven testing)** : if the application to be tested has 10 input parameters, and each can take 5 values, 10^5 input cases must be tested.

Black Box:
- Exploits the apparent simplicity of the software
- Makes assumptions about the implementation
- Suitable for testing interactions between components
- Tests interfaces and behavior

# Black-box testing techniques

- Black-box testing is performed **without** knowing the source.
- It consists of using the product specification to prepare a set of test cases that maximizes the probability of finding an error and minimizes the probability that two different tests will find the same error
- **Equivalence testing with boundary value analysis:** the possible input and/or output data (defined by the specification) can sometimes be partitioned into equivalence classes; in this way the number of test cases needed is reduced and “boundary values” can be used to guide the test.
- **Functional testing:** after having identified in the specification all the functions of a module, the test data needed to check each function separately is defined.

# White Box
- Exploits the internal complexity of the software
- Requires complete knowledge of the implementation
- Suitable for testing single functions
- Tests the implementation and the design

White-box testing techniques:
- **Statement coverage** : each command is executed at least once (but there is no guarantee that every condition is tested).
- **Branch coverage** : each command is executed at least once and every condition is tested.
- **Path coverage** : each possible path is tested at least once.

# Weyuker's Theorem

Given a generic program P, the following are undecidable:
- Is there an input data of P that causes the execution of a particular command? undecidable
- Is there an input data that causes the execution of a particular condition (branch)? undecidable
- Is there an input data that causes the execution of a particular path in P? undecidable

However, it is possible to identify decidable subproblems.

# Code coverage criteria
- command coverage
- decision coverage
- condition coverage
- decision and condition coverage
- path coverage
- n-loop coverage

Command coverage:
Command coverage criterion (statement test): a test T satisfies the command coverage criterion if and only if every executable command of the program is executed on at least one test data in T. In the program control graph, every node corresponding to an executable command must be traversed at least once.

# Test Driven Development: XP

The XP method puts testing **before** coding ( _Test Driven Development: TDD_ ): no module is developed before at least one correctness test has been defined.

Loop:
Test **red** : test for new empty function; test that fails because the function does not exist;
Test **green** : code needed to pass the red test;
**Refactoring** : changes to the green test code to simplify it

# Crowdsourced testing

- Testing managed by non-specialists via cloud infrastructure
- Used for user-centric software especially to evaluate its usability
- Only errors found are paid

Fault injection:
- A technique to improve test coverage by introducing errors to test in particular the code that handles such errors, which otherwise would not be executed
- Example: in the test of an operating system kernel you can insert a driver that intercepts system calls and randomly returns an error for some of the calls.

Testing tools:
- Junit, xunit
- Jenkins
- Selenium
- sonarqube

SonarQube: static analysis
SonarQube is an open platform, extensible with plugins.
It is used to analyze large codebases, reporting bugs and smells.
It covers more than 20 different languages.

# Technical Debt

_Technical Debt_ is an expression that designates the consequences of deliberately accepting a non-optimal development solution to save time, which will however need to be “spent” sooner or later, after the first deployment, perhaps with interest.

# Conclusions

- Software quality is measured with respect to both functional and extra-functional requirements, including source code quality.
- Testing measures functional quality above all with respect to requirements.
- There are many measurable extra-functional qualities: they include, for example, performance, modifiability, maintainability, etc.
- Code quality (e.g. readability, modifiability, etc.) is measured with specific tools, also capable of calculating technical debt.

Self-test questions:
- What is the first thing to do when someone reports that a software product has a bug?
- How is the “quality” of a software product defined?
- How can software quality attributes, such as correctness, maintainability, reliability, be measured?
- What is the difference between verification and validation?
- Using the GQM approach, how could one control the quality of a development process? and that of a UML specification?
- What are the “white box” testing techniques?

# Software Evolution

Lesson Objective:
- Types of software evolution
- Maintenance in the software life cycle
- Economic impact of maintenance
- Maintenance tools
- Useful metrics for maintenance

Software evolution: synonyms:
- Reengineering
- Maintenance
- Updating
- Adaptation
- Refactoring
- Architectural transformation

# Modifying the code

To modify a piece of software, you need to be able to read it.
Reading a program is more difficult than writing it.
Modifying it *without introducing errors* is even more difficult, if you don't have regression tests.

# Software Evolution

- The need for changes before (during development) and after deployment is the only constant factor in the different life cycles of the software
- Successful software products are those that adapt to the continuous changes in the requirements requested by stakeholders
- Notabene: Designing the evolution of software often means designing the evolution of a family of products or systems, rather than a single system

How a software product evolves: releases

Software products generally exist in multiple development versions, called **releases** ( _release_ , in English).
- _Current release_ : contains incremental improvements and adjustments, based on reports from users reporting defects
- _Field release_ ( _fielded_ ): contains urgent repairs made at the user's site to keep the software system operational
- _Release on demand_ (e.g. _alpha product_ ): product that contains new features to be tested and validated before including them in the current release
- _In itinere release_ (e.g. _beta product_ ): product that is complete but not yet fully tested, and not necessarily to be distributed to all users

# After development

- The software is released, and begins its operational life with the users
- The operational software may be subject to change requests, for various reasons
- Changes after release are maintenance activities

Types of software maintenance:
- Corrective maintenance
- Perfective maintenance
- Adaptive maintenance
- Emergency maintenance
- Preventive maintenance

Types of software maintenance:
- Modifying a software product after deployment is normal
- During use, new requirements emerge (perfective m.)
- The operating environment of the software changes or new hardware is added or performance and reliability need to be improved (adaptive m.)
- Errors that emerge during use need to be repaired (corrective m.)
- All organizations have the problem of managing their legacy systems, i.e. software systems whose usefulness persists over time - even decades!
- The management of software product families (Software Product Lines) also requires effective techniques to manage their evolution.

# Fixing errors

- **Preventive** maintenance
- Identifies and removes latent errors, before they are found
- Adapts to systems with security problems
- **Corrective** maintenance
- Identifies and removes defects found during use
- Corrects residual errors after pre-delivery testing
- **Emergency** maintenance
- Unpredictable and urgent corrective maintenance
- Risky because it involves reduced testing

# Development maintenance

- **Perfective** maintenance
- Improves performance, reliability, maintainability
- Adds new features upon customer request
- **Adaptive** maintenance
- Development or migration
- Adapts to a new environment (hw, operating system, middleware)

The cost of maintenance:
The incidence of maintenance on the overall development cost of a system increases over time (second Lehman Law) and can reach up to 80%, of which:
- Corrective maintenance: 20%
- Adaptive maintenance: 25%
- **Perfect** maintenance: 55%

The majority of costs are attributable to changes imposed by the environment (Lehman's 1st Law).

# Maintenance cost factors

- Personnel instability
- Maintenance costs increase if the personnel changes frequently
- Designer irresponsibility
- If the system developers do not have maintenance responsibilities there is no incentive to “ _design for change_ ”
- Personnel inexperience
- Maintenance personnel are often inexperienced and have little knowledge of the application domain
- Age and structure of the software
- As the program ages its structure degrades and becomes more difficult to understand and modify

# Cyclomatic complexity of a module

- The cyclomatic complexity of a module is an excellent indicator of its testability
- A typical application of the cyclomatic complexity of a module is the following **risk value scale**

- Cyclomatic complexity can be used for:
- **Code writing risk analysis**
- **Change risk analysis during maintenance**. Code complexity increases over time due to maintenance. By measuring cyclomatic complexity before and after a change, you can monitor the system configuration and decide how to minimize the risk of further changes
- **Reengineering**. Cyclomatic complexity analysis evaluates the structure of a system: therefore, the risk of reengineering a part of the code is related to its complexity.

Cyclomatic complexity can be used during testing:
- Defines the number of independent paths to test.
- _Path coverage set_ = set of paths that will execute all commands and evaluate all logical conditions at least once.
- Goal: define a minimal set of test cases that «cover» all instructions.
- The _Path coverage set_ is not unique!

# Maintainability Metrics
- Maintainability is the extent to which a software system allows for changes to extend its lifetime.
- Perspectives on maintainability:
- **Internal:** Depends only on the characteristics of the system.
- **External:** Also depends on the maintenance personnel, support environment, documentation, and tools available.

Lower values ​​are better:
- Amount of human resources needed (maintainers)
- Number of people needed (maintainers) / code size
- Time to build, run, and test
- Cyclomatic complexity of the code
- Number of versions to maintain
- Average time to make a change
- Average cost to fix a defect after release
- Number of object files recompiled after a change to a source file
- Amount of dead code, % of dead code on total LOC
- Degree of coupling between modules

Higher values ​​are better:
- Number of design patterns used
- Level of programming language
- Ratio of comment lines to lines of code
- Number of regression tests
- Percentage of maintainers who say the code is easily changeable
- Ratio of number of modules to code size
- Number of high-cohesion modules on total modules

Tools
- There are several tools that can support software maintenance
- Many record useful metrics to evaluate the maintainability index

# Course Conclusions

Course purpose:
To present and experiment with _methods_ and _tools_ for:
- analysis,
- modeling,
- design, and
- measurement
of software systems and applications.

What we have seen:
- Software production standards
- The life cycle of software products
- Agile and Scrum models
- Software modeling with UML
- Requirements analysis and specification
- Software design
- Design patterns
- Software project management: time and costs
- Control and measure software quality

Software is a social construct

- Develop alone?
- Develop in pairs?
- Develop in groups?
- Develop in many?

We are discovering better ways to build software by doing it and helping others to do it. We value Individuals and interactions, Software that works, Collaboration with the customer, Reacting to change (Agile Manifesto).

Conway's Law: Architecture reflects the structure of the organization that builds a system.
Software is the product of a social process, and embodies its structure.