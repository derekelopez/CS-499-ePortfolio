

\# Enhancement One: Software Design and Engineering



\## Smart Thermostat — Raspberry Pi



\### Project Overview



This project originated in CS-350: Emerging Systems Architectures and Technologies at Southern New Hampshire University. The original application was a Python-based smart thermostat designed to operate on a Raspberry Pi using temperature and humidity monitoring, physical button controls, status LEDs, and an LCD display.



The thermostat uses three operating states: OFF, HEAT, and COOL. Physical buttons allow the user to change the operating state and adjust the temperature setpoint.



For the CS-499 Computer Science Capstone, I enhanced the original application by refactoring its architecture into a modular, maintainable software system.



\## Original Artifact



The original implementation was primarily contained in one Python file:



`Original/Derek\_Lopez\_Thermostat.py`



Although the application demonstrated embedded systems programming, its tightly coupled structure made maintenance, testing, and future enhancements more difficult.



Hardware operations, application state management, and configuration values were closely associated within the original implementation.



\## Software Engineering Enhancement



The enhanced implementation separates the application into components with clearly defined responsibilities.



\### Enhanced Architecture



| File | Responsibility |

|---|---|

| `config.py` | Centralized application configuration and operating parameters |

| `thermostat\_core.py` | Thermostat state management and temperature setpoint logic |

| `hardware\_pi.py` | Raspberry Pi GPIO, buttons, LEDs, and LCD hardware interaction |

| `main.py` | Application initialization and main execution loop |



This modular structure reduces coupling and improves readability, maintainability, and testability.



\### Key Improvements



\*\*Modular Design\*\*



The original implementation was refactored into separate modules to isolate hardware-specific functionality from application logic.



\*\*Configuration Management\*\*



Application settings, including GPIO assignments, default temperature setpoints, and operating parameters, were centralized to reduce hardcoded values.



\*\*Input Validation\*\*



Temperature setpoints are constrained to a configured operating range to prevent invalid user input.



\*\*Preserved State Machine\*\*



The original OFF, HEAT, and COOL operating states were retained while improving the organization of state transitions and control logic.



\*\*Maintainability\*\*



Descriptive names, organized functions, and separation of responsibilities make the application easier to extend and troubleshoot.



\*\*Testability\*\*



Separating thermostat logic from hardware interaction allows core functionality to be tested independently of the Raspberry Pi hardware.



\## Testing and Verification



The enhanced application was tested using the Raspberry Pi hardware and physical input/output components.



| Test | Result |

|---|---|

| LCD displays temperature, humidity, state, and setpoint | Passed |

| State button cycles OFF → HEAT → COOL → OFF | Passed |

| Increase button adjusts temperature setpoint | Passed |

| Decrease button adjusts temperature setpoint | Passed |

| Red LED pulses during heating requests | Passed |

| Blue LED pulses during cooling requests | Passed |

| Application exits cleanly using Ctrl+C | Passed |



The enhanced application successfully preserved the original thermostat functionality while improving its internal software architecture.



\## Design Decisions and Trade-Offs



Separating application logic into modules introduces additional files and interfaces compared with the original single-file implementation.



However, this approach improves maintainability and supports independent testing, troubleshooting, and future extensions.



The design also separates the hardware-dependent components from the thermostat's core state-management logic, supporting reuse of the logic in other environments.



\## Security and Reliability Considerations



The enhanced design uses configuration-based setpoint limits to reduce invalid operating inputs.



Separating responsibilities also makes it easier to review and modify individual components without changing unrelated functionality.



The thermostat remains a prototype and should not be considered a production-certified heating or cooling controller. Additional safeguards, fault handling, and hardware-specific validation would be necessary for production use.



\## CS-499 Course Outcomes



This enhancement demonstrates several program outcomes:



1\. \*\*Collaboration and decision-making:\*\* Modular organization and documentation improve code readability and support maintainable development.

2\. \*\*Professional communication:\*\* The project documents architecture changes, design decisions, and testing outcomes.

3\. \*\*Computing solutions:\*\* State-machine logic and input validation implement deterministic thermostat control behavior.

4\. \*\*Computing tools and practices:\*\* Python, Raspberry Pi GPIO, modular design, and iterative hardware verification demonstrate practical software engineering techniques.

5\. \*\*Security mindset:\*\* Input validation, clear component boundaries, and consideration of operational risks support more reliable system design.



\## Connection to Enhancement Three



The thermostat was subsequently extended to support remote telemetry using a Flask API and MongoDB.



The database enhancement is documented separately under `Enhancement-Three-Databases`.



\## Project Files



\- \[Original thermostat source](Original/Derek\_Lopez\_Thermostat.py)

\- \[Enhanced configuration](Enhanced/config.py)

\- \[Enhanced hardware interface](Enhanced/hardware\_pi.py)

\- \[Enhanced application entry point](Enhanced/main.py)

\- \[Enhanced thermostat core](Enhanced/thermostat\_core.py)

\- \[Core unit tests](Enhanced/tests/test\_thermostat\_core.py)



\## Conclusion



Enhancement One transformed the original Raspberry Pi thermostat into a more modular and maintainable embedded software application.



The improvements demonstrate software engineering principles, including separation of concerns, configuration management, input validation, testability, and systematic verification.



