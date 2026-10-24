

\# Enhancement Three: Databases



\## Smart Thermostat — Flask REST API and MongoDB Telemetry



\### Project Overview



This project builds upon the Raspberry Pi Smart Thermostat originally developed in CS-350: Emerging Systems Architectures and Technologies at Southern New Hampshire University.



The original thermostat monitored temperature and humidity, managed OFF, HEAT, and COOL operating states, and interacted with physical hardware through GPIO, buttons, LEDs, and an LCD display.



Although the original application supported local monitoring and control, it did not provide persistent database storage or remote access to historical telemetry.



For the CS-499 Computer Science Capstone, I extended the thermostat into a distributed telemetry system using a Python Flask REST API and MongoDB.



The enhanced system demonstrates communication between an embedded client and a database-backed server.



\## Original Artifact



The original application was implemented in:



`../Enhancement-One-Software-Engineering/Original/Derek\_Lopez\_Thermostat.py`



The original artifact did not include a persistent telemetry database.



Enhancement Three introduces new components that extend the original thermostat rather than replacing its core operating functionality.



\## System Architecture



The enhanced system uses a client-server architecture with three main components:



1\. Raspberry Pi thermostat application.

2\. Flask REST API hosted on a Windows computer.

3\. MongoDB database running on the Windows host.



\### Data Flow



&#x20;   Raspberry Pi Smart Thermostat

&#x20;                |

&#x20;                | Temperature, humidity,

&#x20;                | state, and setpoint

&#x20;                |

&#x20;                v

&#x20;         Telemetry Client

&#x20;                |

&#x20;                | HTTP POST

&#x20;                v

&#x20;         Flask REST API

&#x20;                |

&#x20;                | Validation and processing

&#x20;                v

&#x20;         MongoDB Database

&#x20;                |

&#x20;                | Persistent readings

&#x20;                v

&#x20;         Data retrieval and analysis



The Raspberry Pi collects telemetry from the thermostat application and sends the information to the Flask API.



The server validates incoming data and stores accepted readings in MongoDB.



This design separates embedded hardware operations from database storage and server-side processing.



\## Database Enhancement Components



\### Raspberry Pi Telemetry Client



File: `Enhanced/embedded/telemetry\_client.py`



The telemetry client handles communication between the Raspberry Pi and the Windows-hosted Flask API.



Its responsibilities include:



\- Preparing thermostat readings for transmission.

\- Sending readings to the API.

\- Processing server responses.

\- Handling communication failures.



Separating telemetry communication from the thermostat's core state-management logic helps preserve modularity.



\### Flask REST API



File: `Enhanced/server/app.py`



The Flask application provides REST endpoints for communication and telemetry management.



The implemented API includes:



| HTTP Method | Endpoint | Purpose |

|---|---|---|

| GET | `/api/health` | Check API service health |

| POST | `/api/readings` | Submit thermostat telemetry |



The application provides the interface between the embedded telemetry client and the database layer.



\### MongoDB Integration



File: `Enhanced/server/database.py`



MongoDB provides persistent storage for thermostat readings.



The database integration manages connectivity and operations associated with telemetry records.



MongoDB was selected because its document-oriented structure is suitable for structured telemetry records and supports future extensions to the recorded fields.



\### Input Validation



File: `Enhanced/server/validation.py`



The validation layer separates data checks from the primary API routes and database operations.



Validation is important because incoming network requests must not be assumed to contain valid or trustworthy information.



By maintaining validation responsibilities in a dedicated module, the architecture supports more consistent data handling.



\## Telemetry Information



Thermostat readings include information such as:



\- Temperature.

\- Humidity.

\- Operating state (OFF, HEAT, or COOL).

\- Temperature setpoint.



These values provide a record of the thermostat's measured conditions and operating behavior.



Historical records can support troubleshooting, operational analysis, and future visualization features.



\## Development and Testing



The database enhancement was developed and tested using a Windows-hosted Flask API, a MongoDB service, and the Raspberry Pi thermostat.



\### API Verification



The Flask service was tested using its health and readings endpoints.



The `/api/health` endpoint was used to confirm the API was responding.



A POST request to `/api/readings` was successfully processed after the MongoDB service was started.



\### Database Verification



MongoDB was used to inspect stored telemetry records.



The database successfully received thermostat readings transmitted through the API.



\### Raspberry Pi Integration



The telemetry client successfully transmitted readings to the Windows server.



The Raspberry Pi displayed the message:



&#x20;   Telemetry reading sent successfully



MongoDB contained records representing thermostat operation in different states.



\### Testing Summary



| Test | Result |

|---|---|

| Flask health endpoint responds | Passed |

| POST request accepted by API | Passed |

| MongoDB connection established | Passed |

| Readings stored in MongoDB | Passed |

| Raspberry Pi transmits telemetry | Passed |

| Stored records verified | Passed |



These results demonstrate successful end-to-end communication from the embedded application to persistent database storage.



They do not, by themselves, establish production-level reliability or security under all network and failure conditions.



\## Design Decisions and Trade-Offs



\### Client-Server Separation



The embedded application sends telemetry to an independent server rather than connecting directly to MongoDB.



This allows the server to manage database operations and provides a clearer separation between embedded functionality and persistent storage.



The additional network and server components increase deployment complexity compared with local-only storage.



\### MongoDB



MongoDB supports flexible document-oriented storage, which is useful for telemetry records that may evolve.



However, a flexible database schema makes application-side validation particularly important.



\### Flask



Flask provides a lightweight Python framework for implementing REST endpoints.



Its relatively simple architecture was appropriate for the educational prototype.



A production deployment would require additional operational safeguards and deployment configuration.



\## Security and Privacy Considerations



Security was considered when separating the telemetry client, API, and database layers.



The implementation includes a dedicated validation module intended to prevent malformed input from being accepted without appropriate checks.



Additional security considerations include:



\- Restricting database connectivity to authorized systems.

\- Protecting network communication.

\- Avoiding hardcoded credentials.

\- Validating incoming request data.

\- Handling malformed or unexpected requests.

\- Limiting unnecessary exposure of telemetry records.



The successful telemetry tests do not establish that all these protections are implemented.



In particular, authentication, transport encryption, authorization, and production deployment hardening should be verified or added before exposing the service to an untrusted network.



This project is an educational prototype and should not be treated as a production-ready internet-facing telemetry service.



\## CS-499 Course Outcomes



\### 1. Collaboration and Decision-Making



The client-server architecture and separation of responsibilities make it easier for developers to understand individual components and evaluate design decisions.



Documented interfaces support discussions about integration, scalability, and maintainability.



\### 2. Professional Communication



The architecture description, API documentation, source code, and testing evidence communicate the system's functionality and technical design.



\### 3. Algorithmic Design and Evaluation



The implementation separates data collection, validation, transmission, and storage into distinct processing stages.



These design decisions support predictable system behavior and simplify troubleshooting.



\### 4. Computing Techniques and Tools



The project demonstrates the practical use of Python, Flask, REST APIs, MongoDB, and Raspberry Pi hardware.



End-to-end testing verified communication between the embedded system and the database server.



\### 5. Security Mindset



The system incorporates a dedicated validation layer and considers the security risks of database connectivity, externally supplied data, and network communication.



The project also identifies additional protections necessary for production deployment.



\## Project Files



\### Original Artifact



\- \[Original Smart Thermostat](../Enhancement-One-Software-Engineering/Original/Derek\_Lopez\_Thermostat.py)



\### Enhanced Artifact



\- \[Telemetry client](Enhanced/embedded/telemetry\_client.py)

\- \[Flask API](Enhanced/server/app.py)

\- \[Database integration](Enhanced/server/database.py)

\- \[Input validation](Enhanced/server/validation.py)



\### Related Enhancement



\- \[Software Engineering Enhancement](../Enhancement-One-Software-Engineering/README.md)



\## Conclusion



Enhancement Three extended the original Smart Thermostat from a standalone embedded application into a database-connected telemetry system.



By integrating a Raspberry Pi telemetry client, Flask REST API, and MongoDB, I demonstrated the ability to design, implement, and test a distributed computing solution.



The enhancement strengthened my experience with database integration, RESTful services, modular software design, input validation, and end-to-end system verification.



