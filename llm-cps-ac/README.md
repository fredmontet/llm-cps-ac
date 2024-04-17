# TB - OptiBot

_Chatbot for control of heating system._

## General information

- **Student**: [Philippe Marziale](https://gitlab.forge.hefr.ch/philippe.marziale) - philippe.marziale@edu.hefr.ch
- **Supervisor**: [Houda Chabbi](https://gitlab.forge.hefr.ch/houda.chabbi) - houda.chabbi@hefr.ch
- **Supervisor**: [Sébastien Rumley](https://gitlab.forge.hefr.ch/sebastie.rumley) - sebastien.rumley@hefr.ch
- **Principal**: [Frédéric Montet](https://gitlab.forge.hefr.ch/fredmontet) - frederic.montet@hefr.ch
- **Expert**: [Lionel Jaquet](https://gitlab.forge.hefr.ch/ext-lionel.jaquet) - lionel.jaquet@tebicom.ch
- **Expert**: [Geoffrey Papaux](https://gitlab.forge.hefr.ch/ext-geoffrey.papaux) - geoffrey.papaux@gmail.com
- **School & Institute** : [HEIA-FR](https://www.heia-fr.ch/), [iCoSys](https://icosys.ch/)
- **Dates** : from 30.05.2023 to 06.09.2023


## Background

Switzerland faces a significant sustainability and energy conservation challenge, with around 30% of the country's CO2 emissions coming from buildings[^1]. In particular, heating is the main source of energy consumption and emissions in homes, a situation exacerbated by ineffective control of boilers via a simple "heating curve". With current technological advances, there is clearly significant potential for improvement. Furthermore, in order to meet the objectives of the Paris Agreement, the federal government has taken the decision to reduce CO2 emissions to zero net emissions (carbon neutrality) by 2050.

It was against this backdrop that Frédéric Montet, a doctoral student at the Fribourg School of Engineering and Architecture (HEIA-FR) and member of the Institute of Artificial Intelligence and Complex Systems ([iCoSys](https://icosys.ch/)), launched this Bachelor's project in collaboration with the Fribourg start-up [yord.ch](https://www.yord.ch/). The aim of the project is to develop a heating control system based on a Large Language Model (LLM), using two distinct models to manage boiler operations and user interaction. The initiative builds on the results of the semester 6 (PS6) project, entitled [AppGPT](https://gitlab.forge.hefr.ch/philippe.marziale/ps6-appgpt), which used the OpenAI API to connect to various APIs, thus initiating the foundations for the OptiBot project.

Previous research has explored the possibility of a personal assistant to help tenants regulate their energy consumption. However, this approach has largely been abandoned in favour of solutions that do not interact with the user. The advent of LLMs, such as the one powering ChatGPT, could provide an opportunity to revisit this idea. An LLM could offer an enhanced user experience and a novel multimodal interface to help control heating systems.

The project envisages the development of a simplified boiler simulator, an analysis of the use of [OpenAI](https://openai.com/product) APIs or the [LangChain](https://python.langchain.com/en/latest/index.html) framework for an LLM-based heating control system, the creation of a chatbot capable of conversational interaction with the heating control system, and the construction of a boiler control prototype incorporating the simulator and chatbot. In addition, depending on how the project develops, a feasibility report on integrating the system into the control box developed by [yord.ch](https://www.yord.ch/) is also envisaged.

## Objectives

The main objective of this project is to develop an LLM-based heating control system that will optimise the energy consumption of boilers and reduce CO2 emissions in buildings in Switzerland. Ultimately, the aim is to improve the energy efficiency of buildings by offering a more advanced heating control solution, using the capabilities of LLMs to provide a better user experience and an unprecedented multimodal interface.

Thus, several main objectives arise in order to achieve the demand:

1.  Simplified boiler simulator reproducing the main characteristics and behaviour of a boiler.
2.  Analysis report exploring the possibilities offered by the APIs of [OpenAI](https://openai.com/product) or the [LangChain](https://python.langchain.com/en/latest/index.html) framework for developing an LLM-based heating control system.
3.  Chatbot based on the results of the previous analysis, capable of interacting in a conversational manner with users and answering their requests and questions concerning heating control.
4.  Boiler control prototype including points 1 and 3 above.

Depending on the progress of the project, a secondary objective is also envisaged:

5.  Feasibility report for the integration of the system developed on a connected boiler using the control box developed by [yord.ch](https://www.yord.ch/).

As far as the academic framework of this TB is concerned, particular emphasis is placed on the technical aspects of the project (analysis, design and implementation).

|                                                                                                                  ![Bachelor project diagram](docs/divers/Schema_TB_v3.png)                                                                                                                 |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                                                                 *Bachelor project diagram*                                                                                                                                 |
|                                                                           1 - LLM contact with the user (conversation), the latter must know the user (for example using a questionnaire (age, calendar, etc.))                                                                            |
| 2 - The LLMs connect with the yord box (here, simplified operation of data transmission between the various yord elements) and, depending on the indications provided by the LLMs and the data received by the boiler, a reaction takes place with the aim of optimising boiler operation. |


## Content

This repository contains the entire project. The structure of this git is as follows:
- The [src](src) directory contains the main source code for the project.
- The [utils](utils) directory contains utility files, such as a list of commands that may be useful to know for this project or scripts.

This directory structure is used to organise the different elements of the project, grouping documents, source code and utilities in separate directories for better project management and readability.

---

[^1]: https://www.bfe.admin.ch/bfe/fr/home/efficacite/batiments.html
