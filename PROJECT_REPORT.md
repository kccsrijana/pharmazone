# PHARMAZONE - E-COMMERCE PHARMACY PLATFORM

## A Project Report

Submitted to  
**St. Xavier's College, Maitighar**  
Tribhuvan University

In Partial Fulfillment of the Requirements for the  
**Bachelor of Information Management (BIM)**  
6th Semester

---

**Submitted By:**  
Srijana Khatri  
TU Exam Roll No: [Your Roll Number]  
BIM 6th Semester

**Submitted To:**  
Department of Management  
St. Xavier's College, Maitighar  
Kathmandu, Nepal

**Date:** February 2026

---


## STUDENT'S DECLARATION

I hereby declare that the project work entitled "Pharmazone - E-Commerce Pharmacy Platform" submitted to St. Xavier's College, Maitighar, Tribhuvan University, is a record of an original work done by me under the guidance and supervision of [Supervisor Name], and this work has not been submitted elsewhere for the award of any degree or diploma.

All the information sources used in this project have been duly acknowledged.

---

**Signature:** ___________________  
**Name:** Srijana Khatri  
**Date:** February 2026

---


## SUPERVISOR'S RECOMMENDATION

This is to certify that Srijana Khatri, a student of Bachelor of Information Management (BIM) 6th Semester at St. Xavier's College, Maitighar, has completed the project work entitled "Pharmazone - E-Commerce Pharmacy Platform" under my guidance and supervision.

The project work is original and has been completed satisfactorily. I recommend this project report for evaluation.

---

**Signature:** ___________________  
**Name:** [Supervisor Name]  
**Designation:** [Designation]  
**Date:** February 2026

---


## APPROVAL SHEET

This project work entitled "Pharmazone - E-Commerce Pharmacy Platform" submitted by Srijana Khatri in partial fulfillment of the requirements for the Bachelor of Information Management (BIM) 6th Semester has been approved.

---

**Project Supervisor**  
Signature: ___________________  
Name: [Supervisor Name]  
Date: February 2026

---

**Internal Examiner**  
Signature: ___________________  
Name: [Examiner Name]  
Date: February 2026

---

**External Examiner**  
Signature: ___________________  
Name: [Examiner Name]  
Date: February 2026

---

**Head of Department**  
Signature: ___________________  
Name: [HOD Name]  
Date: February 2026

---


## ACKNOWLEDGEMENT

I would like to express my sincere gratitude to all those who have contributed to the successful completion of this project.

First and foremost, I am deeply grateful to my project supervisor, [Supervisor Name], for their invaluable guidance, continuous support, and constructive feedback throughout the development of this project. Their expertise and encouragement have been instrumental in shaping this work.

I extend my heartfelt thanks to St. Xavier's College, Maitighar, and the Department of Management for providing the necessary resources and conducive environment for completing this project.

I am thankful to all the faculty members of the BIM program who have imparted knowledge and skills that have been essential in developing this e-commerce platform.

I would also like to acknowledge the support of my family and friends who have been a constant source of motivation and encouragement throughout this journey.

Finally, I am grateful to all the developers and contributors of open-source technologies, particularly Django, Bootstrap, and other frameworks used in this project, whose work has made this development possible.

---

**Srijana Khatri**  
BIM 6th Semester  
February 2026

---


## ABSTRACT

Traditional pharmacy shopping in Nepal faces challenges including limited accessibility, time constraints, and lack of digital payment options. Pharmazone is a comprehensive e-commerce pharmacy platform that addresses these issues by enabling users to browse medicines, place orders, make secure payments, and access healthcare consultations online.

Built using Django framework with Python, the system follows the Model-View-Template (MVT) architecture and incorporates HTML5, CSS3, Bootstrap 5, and JavaScript for a responsive interface. Key features include a medicine catalog with search functionality, shopping cart, eSewa payment gateway integration, Cash on Delivery option, order tracking, and automated PDF invoice generation.

The platform integrates healthcare services including doctor appointment booking and pharmacist chat consultations. It implements role-based access control for customers and administrators, with security measures including secure admin authentication, encrypted payment processing, and input validation. The admin dashboard provides medicine inventory management, order processing, appointment scheduling, and business analytics with email notifications for order confirmations.

This project demonstrates practical application of software engineering principles, database design, payment gateway integration, and user experience design in developing a real-world e-commerce solution for the Nepali healthcare market.

**Keywords:** E-commerce, Online Pharmacy, Django, Payment Gateway, Healthcare Services, eSewa Integration, Doctor Appointments, Medicine Delivery

---


## TABLE OF CONTENTS

**TITLE PAGE** .............................................................................................i

**STUDENT'S DECLARATION** .....................................................................ii

**SUPERVISOR'S RECOMMENDATION** ........................................................iii

**APPROVAL SHEET** ....................................................................................iv

**ACKNOWLEDGEMENT** ...............................................................................v

**ABSTRACT** .................................................................................................vi

**TABLE OF CONTENTS** ..............................................................................vii

**LIST OF TABLES** ........................................................................................ix

**LIST OF FIGURES** .......................................................................................x

**LIST OF ABBREVIATIONS** .........................................................................xi

---

**CHAPTER I: INTRODUCTION** ....................................................................1
- 1.1 Background of the Project...................................................................1
- 1.2 Problem Statement...............................................................................2
- 1.3 Objectives of the Project......................................................................3
- 1.4 Literature Review..................................................................................3
- 1.5 Development Methodology....................................................................7
- 1.6 Scope and Limitations...........................................................................9
- 1.7 Report Organization............................................................................10

**CHAPTER II: SYSTEM DEVELOPMENT PROCESS** ....................................11
- 2.1 Analysis..............................................................................................11
- 2.2 Design.................................................................................................27
- 2.3 Implementation....................................................................................39
- 2.4 Deployment..........................................................................................44

**CHAPTER III: CONCLUSION AND RECOMMENDATION** ..........................45
- 3.1 Summary.............................................................................................45
- 3.2 Conclusion...........................................................................................47
- 3.3 Recommendations................................................................................48

**REFERENCES** .............................................................................................49

**APPENDICES** ..............................................................................................51

---


# CHAPTER I: INTRODUCTION

## 1.1 Background of the Project

The healthcare industry has witnessed a significant digital transformation in recent years, with e-commerce platforms revolutionizing how people access medicines and healthcare services. In Nepal, the traditional method of purchasing medicines involves physically visiting pharmacies, which can be time-consuming, inconvenient, and challenging for patients with mobility issues or those living in remote areas. The COVID-19 pandemic further highlighted the need for contactless healthcare solutions and online medicine delivery services.

Pharmazone is an e-commerce pharmacy platform developed to address these challenges by providing a comprehensive digital solution for medicine procurement and healthcare consultations. The platform enables customers to browse a wide range of medicines, place orders online, make secure payments, and have medicines delivered to their doorstep. Beyond basic e-commerce functionality, Pharmazone integrates additional healthcare services including doctor appointment booking and pharmacist consultations, making it a holistic healthcare solution.

The project is developed as part of the Bachelor of Information Management (BIM) 6th Semester curriculum at St. Xavier's College, Maitighar. It demonstrates the practical application of software engineering principles, database management, web development technologies, and payment gateway integration in creating a real-world e-commerce solution tailored for the Nepali market.

The platform is built using Django, a high-level Python web framework known for its security features, scalability, and rapid development capabilities. The system follows the Model-View-Template (MVT) architectural pattern and incorporates modern web technologies to deliver a responsive, user-friendly interface that works seamlessly across desktop and mobile devices.

Pharmazone serves two primary user groups: customers who purchase medicines and book appointments, and administrators who oversee the entire platform. The system implements robust security measures including role-based access control, secure payment processing through eSewa integration, and proper data validation to ensure user privacy and transaction security.

---

## 1.2 Problem Statement

The traditional pharmacy system in Nepal faces several challenges that affect both customers and pharmacy businesses:

**1. Limited Accessibility:** Customers, especially those in remote areas or with mobility constraints, face difficulties accessing pharmacies. Elderly patients and individuals with chronic conditions requiring regular medication find it challenging to visit pharmacies frequently.

**2. Time Constraints:** Working professionals and busy individuals struggle to find time during pharmacy operating hours to purchase medicines. Long queues and waiting times at physical pharmacies add to the inconvenience.

**3. Medicine Availability:** Customers often visit multiple pharmacies to find specific medicines, wasting time and effort. There is no centralized system to check medicine availability before visiting a pharmacy.

**4. Lack of Information:** Customers have limited access to comprehensive medicine information, including composition, side effects, contraindications, and proper usage instructions. This information gap can lead to improper medication use.

**5. Healthcare Consultation Barriers:** Access to doctors for consultations is limited by appointment availability, travel requirements, and consultation fees. Patients often need quick advice about minor health issues but cannot easily reach healthcare professionals.

**6. Payment Limitations:** Traditional pharmacies primarily accept cash payments, which is inconvenient for customers who prefer digital payment methods. There is a lack of integrated digital payment solutions in pharmacy services.

**7. Order Tracking:** Customers have no way to track their medicine orders or delivery status, leading to uncertainty and inconvenience.

**8. Record Management:** Manual record-keeping in traditional pharmacies is prone to errors, makes it difficult to track purchase history, and provides no easy way for customers to access their past prescriptions and orders.

**9. Business Management:** Pharmacy owners face challenges in inventory management, order processing, and business analytics without proper digital tools.

**10. Prescription Verification:** Ensuring proper prescription verification for controlled medicines while maintaining customer convenience is a significant challenge.

These problems necessitate a comprehensive digital solution that can bridge the gap between customers and pharmacy services while ensuring security, convenience, and regulatory compliance. Pharmazone addresses these challenges by providing an integrated e-commerce platform with healthcare services, secure payment processing, and efficient business management tools.

---

## 1.3 Objectives of the Project

The primary objective of this project is to develop a comprehensive e-commerce pharmacy platform that provides convenient access to medicines and healthcare services. The specific objectives are:

**Primary Objectives:**

1. To develop a user-friendly web-based platform for online medicine purchasing and delivery
2. To integrate secure payment gateway (eSewa) for digital transactions
3. To implement a comprehensive medicine catalog with search and filtering capabilities
4. To create an efficient order management and tracking system
5. To provide healthcare consultation services through doctor appointments and pharmacist chat

**Secondary Objectives:**

1. To implement role-based access control for customers and administrators
2. To develop an admin dashboard for business management and analytics
3. To create an automated invoice generation system
4. To implement email notification system for order confirmations and updates
5. To ensure responsive design for seamless access across devices
6. To maintain security and privacy of user data and transactions
7. To provide prescription upload and verification functionality
8. To create a scalable and maintainable system architecture

**Learning Objectives:**

1. To apply software engineering principles in real-world application development
2. To gain practical experience in web development using Django framework
3. To understand e-commerce business logic and payment gateway integration
4. To implement database design and management for complex systems
5. To develop skills in user interface design and user experience optimization

---

## 1.4 Literature Review

### 1.4.1 Overview of Existing Systems

The online pharmacy industry has grown significantly worldwide, with several established platforms providing medicine delivery services. Understanding existing systems helps identify best practices and areas for improvement.

**International Systems:**

1. **1mg (India):** One of India's leading online pharmacy platforms offering medicine delivery, lab tests, and doctor consultations. It features a comprehensive medicine database, prescription management, and multiple payment options. The platform uses AI-powered medicine search and provides detailed medicine information.

2. **PharmEasy (India):** A popular healthcare platform providing medicine delivery, diagnostic tests, and teleconsultation services. It offers subscription-based medicine delivery for chronic conditions and integrates with insurance providers.

3. **Netmeds (India):** An online pharmacy with a wide medicine catalog, prescription upload facility, and doorstep delivery. It provides medicine reminders, health articles, and wellness products.

4. **CVS Pharmacy (USA):** A major pharmacy chain with robust online presence offering prescription refills, medicine delivery, and health services. It integrates with health insurance and provides medication management tools.

**Nepali Context:**

In Nepal, the online pharmacy sector is still emerging. A few platforms have started offering medicine delivery services, but most lack comprehensive features like integrated payment gateways, doctor consultations, and advanced order management. Traditional pharmacies dominate the market, with limited digital presence.

**Key Features in Existing Systems:**

- Medicine catalog with search and filtering
- Prescription upload and verification
- Shopping cart and checkout process
- Multiple payment options
- Order tracking and history
- User accounts and profiles
- Medicine reminders and refill alerts
- Health articles and information
- Customer reviews and ratings
- Loyalty programs and discounts

**Gaps Identified:**

1. Limited integration of payment gateways in Nepali context
2. Lack of comprehensive healthcare services (appointments, consultations)
3. Insufficient focus on user experience and interface design
4. Limited admin tools for business management
5. Absence of automated invoice generation
6. Inadequate security measures for admin access

### 1.4.2 Technologies Used in Similar Systems

Modern e-commerce pharmacy platforms utilize various technologies to deliver robust, scalable, and secure services:

**Backend Technologies:**

1. **Django (Python):** Used by many healthcare platforms for its security features, ORM capabilities, and rapid development. Django's built-in authentication, admin interface, and form handling make it ideal for e-commerce applications.

2. **Node.js with Express:** Popular for real-time features and scalable applications. Used in platforms requiring high concurrency and real-time updates.

3. **Ruby on Rails:** Known for convention over configuration, used in several healthcare startups for rapid prototyping and development.

4. **PHP with Laravel:** Widely used in e-commerce platforms for its extensive ecosystem and ease of deployment.

**Frontend Technologies:**

1. **React.js:** Used for building dynamic, single-page applications with excellent user experience
2. **Vue.js:** Lightweight framework for progressive web applications
3. **Bootstrap:** CSS framework for responsive design and consistent UI components
4. **jQuery:** For DOM manipulation and AJAX requests

**Database Systems:**

1. **PostgreSQL:** Preferred for production environments due to reliability and advanced features
2. **MySQL:** Widely used for its performance and ease of use
3. **MongoDB:** NoSQL database for flexible schema and scalability
4. **SQLite:** Used in development and small-scale applications

**Payment Gateway Integration:**

1. **eSewa (Nepal):** Leading digital wallet and payment gateway in Nepal
2. **Khalti (Nepal):** Popular mobile wallet for digital payments
3. **Stripe:** International payment processing platform
4. **PayPal:** Widely used for online transactions globally

**Additional Technologies:**

1. **Redis:** For caching and session management
2. **Celery:** For asynchronous task processing
3. **AWS/Azure:** Cloud hosting and storage services
4. **Docker:** For containerization and deployment
5. **Nginx/Apache:** Web servers for production deployment

### 1.4.3 Theoretical Background

**E-Commerce Architecture:**

E-commerce platforms typically follow a three-tier architecture:

1. **Presentation Layer:** User interface that customers interact with, built using HTML, CSS, and JavaScript
2. **Application Layer:** Business logic layer handling user requests, processing data, and managing workflows
3. **Data Layer:** Database management system storing user data, products, orders, and transactions

**Model-View-Template (MVT) Pattern:**

Django follows the MVT architectural pattern, a variation of the Model-View-Controller (MVC) pattern:

1. **Model:** Defines data structure and database schema, handles data validation and business logic
2. **View:** Processes user requests, interacts with models, and returns responses
3. **Template:** Presentation layer that renders HTML with dynamic data

**Payment Gateway Integration:**

Payment gateway integration involves several steps:

1. **Initiation:** Customer selects payment method and initiates transaction
2. **Redirection:** User is redirected to payment gateway with encrypted transaction details
3. **Authentication:** Payment gateway authenticates user and processes payment
4. **Callback:** Gateway sends success/failure response to merchant application
5. **Verification:** Merchant verifies transaction authenticity and updates order status
6. **Confirmation:** Customer receives confirmation and invoice

**Security Principles:**

1. **Authentication:** Verifying user identity through credentials
2. **Authorization:** Controlling access based on user roles and permissions
3. **Data Encryption:** Protecting sensitive data during transmission and storage
4. **Input Validation:** Preventing SQL injection and XSS attacks
5. **CSRF Protection:** Preventing cross-site request forgery attacks
6. **Session Management:** Secure handling of user sessions

**Database Design Principles:**

1. **Normalization:** Organizing data to reduce redundancy
2. **Relationships:** Defining one-to-one, one-to-many, and many-to-many relationships
3. **Indexing:** Improving query performance
4. **Constraints:** Ensuring data integrity through primary keys, foreign keys, and unique constraints

### 1.4.4 Research Papers and Related Work

Several research studies have explored online pharmacy systems, e-commerce platforms, and healthcare digitalization:

**1. "Design and Implementation of Online Pharmacy Management System"**
- Authors: Various researchers in healthcare IT
- Key Findings: Online pharmacy systems improve medicine accessibility, reduce operational costs, and enhance customer satisfaction. Integration of prescription verification and secure payment processing are critical success factors.

**2. "E-Commerce in Healthcare: Opportunities and Challenges"**
- Focus: Digital transformation in healthcare sector
- Insights: E-commerce platforms in healthcare face unique challenges including regulatory compliance, prescription verification, and maintaining patient privacy. Success requires balancing convenience with security.

**3. "Payment Gateway Integration in E-Commerce Applications"**
- Technical Focus: Secure payment processing
- Recommendations: Implement multiple payment options, ensure PCI DSS compliance, use encryption for sensitive data, and implement proper error handling and transaction verification.

**4. "User Experience Design in Healthcare Applications"**
- Research Area: UI/UX in healthcare
- Findings: Healthcare applications require intuitive interfaces, clear information architecture, accessibility features, and mobile responsiveness. User trust is built through professional design and transparent processes.

**5. "Role-Based Access Control in Web Applications"**
- Security Focus: Access control mechanisms
- Best Practices: Implement principle of least privilege, use role hierarchies, maintain audit logs, and regularly review access permissions.

**Relevance to Pharmazone:**

These studies inform the design and implementation of Pharmazone by:
- Emphasizing the importance of secure payment integration
- Highlighting the need for user-friendly interfaces
- Stressing the significance of proper access control
- Demonstrating the value of comprehensive healthcare services
- Providing best practices for e-commerce development

---

## 1.5 Development Methodology

Pharmazone follows the Iterative Waterfall Model, a systematic approach that combines the structure of the traditional waterfall model with the flexibility of iterative development. This methodology is well-suited for academic projects where requirements are relatively stable but refinements are needed based on testing and feedback.

**Phases of Development:**

### Phase 1: Requirement Analysis and Planning
**Duration:** Week 1-2

**Activities:**
- Identified stakeholders (customers, administrators)
- Gathered functional and non-functional requirements
- Analyzed existing online pharmacy systems
- Defined project scope and objectives
- Created project timeline and resource allocation
- Selected appropriate technologies and tools

**Deliverables:**
- Requirements specification document
- Project proposal
- Technology stack selection
- Project timeline

### Phase 2: System Design
**Duration:** Week 3-4

**Activities:**
- Designed database schema with entity-relationship diagrams
- Created system architecture diagrams
- Designed user interface mockups and wireframes
- Planned URL structure and navigation flow
- Defined data flow diagrams
- Designed security architecture

**Deliverables:**
- Database design documents
- System architecture diagrams
- UI/UX mockups
- Data flow diagrams
- Security design specifications

### Phase 3: Implementation
**Duration:** Week 5-14

**Activities:**
- Set up development environment
- Implemented database models
- Developed user authentication system
- Created medicine catalog and search functionality
- Implemented shopping cart and checkout process
- Integrated eSewa payment gateway
- Developed order management system
- Created invoice generation functionality
- Implemented doctor appointment booking
- Developed pharmacist chat system
- Created admin dashboard and management tools
- Implemented email notification system
- Developed responsive UI with Bootstrap

**Deliverables:**
- Functional web application
- Source code with documentation
- Database with sample data
- Admin panel for management

### Phase 4: Testing
**Duration:** Week 15-16

**Activities:**
- Conducted unit testing for individual components
- Performed integration testing for system modules
- Executed system testing for complete workflows
- Conducted user acceptance testing
- Tested payment gateway integration
- Verified security measures
- Tested responsive design across devices
- Fixed identified bugs and issues

**Deliverables:**
- Test cases and test results
- Bug reports and fixes
- Performance test results
- Security audit report

### Phase 5: Deployment and Documentation
**Duration:** Week 17-18

**Activities:**
- Prepared deployment environment
- Configured production settings
- Created user documentation
- Developed admin manual
- Prepared project report
- Created presentation materials

**Deliverables:**
- Deployed application
- User manual
- Admin documentation
- Project report
- Presentation slides

**Iterative Refinement:**

Throughout the development process, iterative refinements were made based on:
- Testing feedback
- Supervisor guidance
- User experience improvements
- Security enhancements
- Performance optimizations

**Advantages of This Methodology:**

1. **Structured Approach:** Clear phases with defined deliverables
2. **Flexibility:** Ability to refine features based on feedback
3. **Quality Assurance:** Testing integrated throughout development
4. **Documentation:** Comprehensive documentation at each phase
5. **Risk Management:** Early identification and mitigation of issues

---

## 1.6 Scope and Limitations

### 1.6.1 Scope of the Project

**Functional Scope:**

1. **User Management:**
   - User registration and authentication
   - Role-based access (customer, pharmacy, admin)
   - Profile management
   - Password reset functionality

2. **Medicine Catalog:**
   - Comprehensive medicine database
   - Category-based organization
   - Search and filtering capabilities
   - Detailed medicine information
   - Medicine images and descriptions

3. **E-Commerce Features:**
   - Shopping cart functionality
   - Checkout process
   - Multiple payment methods (eSewa, Cash on Delivery)
   - Order tracking and history
   - Order cancellation
   - Refund requests

4. **Payment Processing:**
   - eSewa payment gateway integration
   - Secure payment verification
   - Automatic invoice generation
   - Payment history

5. **Healthcare Services:**
   - Doctor appointment booking
   - Doctor profiles with specializations
   - Appointment scheduling and management
   - Pharmacist chat consultation
   - Quick response system for common queries

6. **Admin Features:**
   - Comprehensive admin dashboard
   - Medicine inventory management
   - Order management and processing
   - Appointment management
   - User management
   - Business analytics and reports

7. **Notifications:**
   - Email notifications for orders
   - Order confirmation emails
   - Payment receipts
   - Appointment confirmations

**Technical Scope:**

1. Web-based application accessible through browsers
2. Responsive design for desktop and mobile devices
3. SQLite database for development
4. Django framework with Python
5. Bootstrap for frontend design
6. eSewa test API integration

### 1.6.2 Limitations of the Project

**Technical Limitations:**

1. **Database:** Uses SQLite for development; requires migration to PostgreSQL for production
2. **Real-time Features:** No real-time chat; pharmacist chat uses request-response model
3. **Mobile App:** No native mobile application; relies on responsive web design
4. **Payment Options:** Limited to eSewa and Cash on Delivery; no credit card or other payment gateways
5. **Scalability:** Current architecture suitable for small to medium scale; requires optimization for large-scale deployment

**Functional Limitations:**

1. **Prescription Verification:** Manual prescription verification; no automated OCR or AI-based verification
2. **Inventory Integration:** No integration with physical pharmacy inventory systems
3. **Delivery Tracking:** No real-time GPS-based delivery tracking
4. **Video Consultation:** No video call feature for doctor consultations
5. **Medicine Reminders:** No automated medicine reminder system
6. **Insurance Integration:** No health insurance claim processing

**Regulatory Limitations:**

1. **Licensing:** Requires proper pharmacy licensing for commercial operation
2. **Controlled Substances:** Limited handling of controlled substances requiring special permits
3. **Medical Advice:** Pharmacist chat provides general information, not medical diagnosis
4. **Data Privacy:** Requires compliance with data protection regulations for commercial use

**Operational Limitations:**

1. **Delivery Coverage:** Delivery service limited to specific geographic areas
2. **Operating Hours:** Admin availability during business hours
3. **Language:** Currently supports English only; no Nepali language support
4. **Customer Support:** Limited to email and chat; no phone support

**Future Enhancement Opportunities:**

These limitations provide opportunities for future enhancements and scalability improvements as the platform grows.

---

## 1.7 Report Organization

This project report is organized into three main chapters, each serving a specific purpose in documenting the development and implementation of the Pharmazone e-commerce pharmacy platform.

**Chapter I: Introduction**

This chapter provides the foundational context for the project. It begins with the background explaining the need for online pharmacy services in Nepal and the motivation behind developing Pharmazone. The problem statement identifies specific challenges in traditional pharmacy systems that the project addresses. The objectives section outlines both primary and secondary goals of the project. The literature review examines existing systems, technologies, and theoretical concepts relevant to e-commerce pharmacy platforms. The development methodology section describes the iterative waterfall approach used in building the system. Finally, the scope and limitations section defines what the project covers and acknowledges its constraints.

**Chapter II: System Development Process**

This chapter details the technical aspects of system development. It is divided into four major sections: Analysis, Design, Implementation, and Deployment. The Analysis section covers requirement gathering, feasibility study, use case diagrams, data flow diagrams, and system requirements specifications. The Design section presents the system architecture, database design with ER diagrams, user interface designs, and system flowcharts. The Implementation section discusses the tools and technologies used, coding standards, security considerations, and testing procedures. The Deployment section describes the deployment process and configuration.

**Chapter III: Conclusion and Recommendation**

This chapter summarizes the project outcomes and provides insights for future work. The Summary section presents key findings, discusses limitations of the current system, suggests future enhancements, and shares lessons learned during development. The Conclusion section reflects on the achievement of project objectives and the overall success of the platform. The Recommendations section provides suggestions for improving the system and expanding its capabilities.

**Additional Sections:**

- **References:** Lists all academic papers, books, websites, and resources consulted during the project
- **Appendices:** Contains supplementary materials including code snippets, additional diagrams, test cases, and user manuals

This organization ensures a logical flow from project conception through implementation to conclusion, making it easy for readers to understand the complete development process and outcomes of the Pharmazone platform.

---


# CHAPTER II: SYSTEM DEVELOPMENT PROCESS

## 2.1 Analysis

The analysis phase involves understanding system requirements, assessing feasibility, and creating structured models that guide the development process. This phase establishes the foundation for successful system implementation.

### 2.1.1 Requirement Analysis

Requirement analysis identifies what the system must do (functional requirements) and how well it must perform (non-functional requirements).

#### Functional Requirements

Functional requirements define the specific behaviors and functions of the Pharmazone system:

**User Management Requirements:**

1. **FR-001:** The system shall allow users to register with email, username, and password
2. **FR-002:** The system shall support two user types: customer and admin
3. **FR-003:** The system shall provide login and logout functionality
4. **FR-004:** The system shall allow users to update their profile information
5. **FR-005:** The system shall provide password reset functionality
6. **FR-006:** The system shall validate email format during registration
7. **FR-007:** The system shall maintain user session for 24 hours

**Medicine Catalog Requirements:**

8. **FR-008:** The system shall display a comprehensive medicine catalog
9. **FR-009:** The system shall organize medicines by categories
10. **FR-010:** The system shall provide search functionality across medicine names
11. **FR-011:** The system shall display medicine details including name, strength, price, and description
12. **FR-012:** The system shall show medicine availability status
13. **FR-013:** The system shall display medicine images
14. **FR-014:** The system shall support filtering by category and price range

**Shopping Cart Requirements:**

15. **FR-015:** The system shall allow customers to add medicines to cart
16. **FR-016:** The system shall allow customers to update cart item quantities
17. **FR-017:** The system shall allow customers to remove items from cart
18. **FR-018:** The system shall display cart total with delivery charges
19. **FR-019:** The system shall persist cart data during user session
20. **FR-020:** The system shall prevent admin users from adding items to cart

**Order Management Requirements:**

21. **FR-021:** The system shall allow customers to place orders
22. **FR-022:** The system shall collect delivery address during checkout
23. **FR-023:** The system shall generate unique order numbers
24. **FR-024:** The system shall support order status tracking
25. **FR-025:** The system shall allow customers to view order history
26. **FR-026:** The system shall allow customers to cancel pending orders
27. **FR-027:** The system shall allow admin to update order status
28. **FR-028:** The system shall maintain order status history

**Payment Processing Requirements:**

29. **FR-029:** The system shall support Cash on Delivery payment method
30. **FR-030:** The system shall integrate eSewa payment gateway
31. **FR-031:** The system shall verify payment transactions
32. **FR-032:** The system shall handle payment success and failure callbacks
33. **FR-033:** The system shall generate invoices automatically after payment
34. **FR-034:** The system shall allow users to download invoices as PDF
35. **FR-035:** The system shall support refund requests

**Doctor Appointment Requirements:**

36. **FR-036:** The system shall display list of available doctors
37. **FR-037:** The system shall show doctor specializations and consultation fees
38. **FR-038:** The system shall allow customers to book appointments
39. **FR-039:** The system shall display available time slots based on doctor schedule
40. **FR-040:** The system shall prevent double booking of time slots
41. **FR-041:** The system shall allow customers to cancel appointments
42. **FR-042:** The system shall allow admin to manage appointments
43. **FR-043:** The system shall support appointment rescheduling

**Pharmacist Chat Requirements:**

44. **FR-044:** The system shall provide pharmacist chat functionality
45. **FR-045:** The system shall display quick response options for common queries
46. **FR-046:** The system shall allow unlimited conversation messages
47. **FR-047:** The system shall maintain chat history
48. **FR-048:** The system shall allow customers to view past chats

**Admin Dashboard Requirements:**

49. **FR-049:** The system shall provide admin dashboard with business metrics
50. **FR-050:** The system shall display total orders, revenue, and appointments
51. **FR-051:** The system shall allow admin to manage medicine inventory
52. **FR-052:** The system shall allow admin to add, edit, and delete medicines
53. **FR-053:** The system shall allow admin to manage orders
54. **FR-054:** The system shall allow admin to manage appointments
55. **FR-055:** The system shall restrict admin access to username 'admin' only

**Notification Requirements:**

56. **FR-056:** The system shall send email notifications for order confirmations
57. **FR-057:** The system shall send email notifications to admin for new orders
58. **FR-058:** The system shall send payment confirmation emails
59. **FR-059:** The system shall send appointment confirmation notifications

#### Non-Functional Requirements

Non-functional requirements define system qualities and constraints:

**Performance Requirements:**

1. **NFR-001:** The system shall load pages within 3 seconds under normal conditions
2. **NFR-002:** The system shall support at least 100 concurrent users
3. **NFR-003:** The system shall process payment transactions within 5 seconds
4. **NFR-004:** The system shall generate invoices within 2 seconds

**Security Requirements:**

5. **NFR-005:** The system shall encrypt user passwords using Django's built-in hashing
6. **NFR-006:** The system shall implement CSRF protection for all forms
7. **NFR-007:** The system shall validate all user inputs to prevent SQL injection
8. **NFR-008:** The system shall implement role-based access control
9. **NFR-009:** The system shall secure payment transactions using HTTPS
10. **NFR-010:** The system shall implement secure admin authentication with triple validation

**Usability Requirements:**

11. **NFR-011:** The system shall provide intuitive navigation with clear menu structure
12. **NFR-012:** The system shall display helpful error messages for user actions
13. **NFR-013:** The system shall provide consistent UI design across all pages
14. **NFR-014:** The system shall be accessible to users with basic computer literacy
15. **NFR-015:** The system shall provide search functionality with autocomplete

**Reliability Requirements:**

16. **NFR-016:** The system shall have 99% uptime during business hours
17. **NFR-017:** The system shall handle errors gracefully without crashing
18. **NFR-018:** The system shall maintain data integrity during transactions
19. **NFR-019:** The system shall backup database regularly
20. **NFR-020:** The system shall log all critical operations for audit

**Compatibility Requirements:**

21. **NFR-021:** The system shall work on Chrome, Firefox, Safari, and Edge browsers
22. **NFR-022:** The system shall be responsive on desktop, tablet, and mobile devices
23. **NFR-023:** The system shall support screen resolutions from 320px to 1920px
24. **NFR-024:** The system shall be compatible with Python 3.8 or higher

**Maintainability Requirements:**

25. **NFR-025:** The system shall follow Django coding conventions
26. **NFR-026:** The system shall include inline code documentation
27. **NFR-027:** The system shall use modular architecture for easy updates
28. **NFR-028:** The system shall separate business logic from presentation
29. **NFR-029:** The system shall use version control (Git) for code management

**Scalability Requirements:**

30. **NFR-030:** The system architecture shall support horizontal scaling
31. **NFR-031:** The system shall be database-agnostic (SQLite for dev, PostgreSQL for production)
32. **NFR-032:** The system shall support caching for improved performance
33. **NFR-033:** The system shall handle increasing data volume efficiently

---

### 2.1.2 Feasibility Study

A feasibility study assesses whether the project is viable from technical, economic, operational, and schedule perspectives.

#### Technical Feasibility

**Assessment:** The project is technically feasible.

**Justification:**
- Django framework provides robust tools for web development
- Python has extensive libraries for payment integration, PDF generation, and email handling
- Bootstrap framework enables responsive design without complex coding
- eSewa provides well-documented API for payment integration
- SQLite is suitable for development and can migrate to PostgreSQL for production
- All required technologies are open-source and well-supported

**Technical Resources Available:**
- Development laptop with adequate specifications
- Internet connection for research and API testing
- Free hosting options for deployment (PythonAnywhere, Heroku)
- Version control using Git and GitHub

**Technical Challenges Identified:**
- Payment gateway integration requires careful handling of callbacks
- Security implementation needs thorough testing
- Responsive design requires testing across multiple devices

**Mitigation Strategies:**
- Follow eSewa documentation and test in sandbox environment
- Implement Django's built-in security features
- Use Bootstrap's responsive grid system and test regularly

#### Economic Feasibility

**Assessment:** The project is economically feasible.

**Cost Analysis:**

**Development Costs:**
- Development tools: Rs. 0 (using free and open-source software)
- Domain name: Rs. 1,500 per year (optional for academic project)
- Hosting: Rs. 0 (using free tier or local development)
- eSewa test account: Rs. 0 (free test environment)
- Total Development Cost: Rs. 0 - 1,500

**Operational Costs (if deployed commercially):**
- Server hosting: Rs. 5,000 - 10,000 per month
- Domain and SSL: Rs. 2,000 per year
- Payment gateway fees: 2-3% per transaction
- Maintenance: Rs. 10,000 per month
- Total Monthly Operational Cost: Rs. 15,000 - 20,000

**Potential Revenue (if commercialized):**
- Commission on medicine sales: 10-15% per order
- Doctor appointment booking fee: Rs. 50-100 per appointment
- Featured medicine listings: Rs. 5,000 per month
- Estimated Monthly Revenue: Rs. 50,000 - 100,000 (with 500-1000 orders)

**Return on Investment:**
- Break-even point: 3-6 months after launch
- Positive ROI expected within first year

**Conclusion:** The project requires minimal investment for development and has potential for profitability if commercialized.

#### Operational Feasibility

**Assessment:** The project is operationally feasible.

**User Acceptance:**
- Growing trend of online shopping in Nepal
- Increased smartphone and internet penetration
- COVID-19 has normalized online medicine purchases
- Convenience of home delivery appeals to customers

**Organizational Readiness:**
- Admin can manage the platform efficiently
- Existing pharmacy inventory can be digitized
- Delivery logistics can be outsourced or managed in-house
- Customer support can be provided through chat and email

**Process Changes Required:**
- Shift from manual to digital order processing
- Implementation of online payment handling
- Integration of delivery management
- Digital inventory tracking

**Stakeholder Support:**
- Customers benefit from convenience and time savings
- Pharmacy owners gain wider market reach
- Doctors can offer consultations with flexible scheduling
- Administrators have better business insights

**Conclusion:** The system aligns with current market trends and user expectations, making it operationally viable.

#### Schedule Feasibility

**Assessment:** The project is feasible within the given timeframe.

**Time Allocation:**

| Phase | Duration | Weeks |
|-------|----------|-------|
| Requirement Analysis | 2 weeks | Week 1-2 |
| System Design | 2 weeks | Week 3-4 |
| Implementation | 10 weeks | Week 5-14 |
| Testing | 2 weeks | Week 15-16 |
| Deployment & Documentation | 2 weeks | Week 17-18 |
| **Total** | **18 weeks** | **4.5 months** |

**Critical Path Analysis:**
- Database design must complete before implementation
- User authentication must complete before other features
- Payment integration requires completed order system
- Testing requires completed implementation

**Risk Factors:**
- Payment gateway integration may take longer than expected
- Bug fixes during testing may extend timeline
- Documentation requires significant time

**Mitigation:**
- Start payment integration early with test environment
- Conduct continuous testing during development
- Document code inline to reduce final documentation time

**Conclusion:** The 18-week timeline is realistic with proper planning and consistent effort.

#### Legal Feasibility

**Assessment:** The project is legally feasible with considerations.

**Regulatory Compliance:**
- Pharmacy licensing required for commercial operation
- Compliance with Nepal's drug regulations
- Data protection and privacy laws must be followed
- Payment gateway compliance with financial regulations

**Intellectual Property:**
- All code is original or uses open-source libraries
- Medicine information sourced from public databases
- No copyright infringement on images or content

**Terms of Service:**
- Clear terms and conditions for users
- Privacy policy for data handling
- Disclaimer for medical information

**Conclusion:** The project is legally feasible for academic purposes. Commercial deployment requires proper licensing and regulatory compliance.

**Overall Feasibility Conclusion:**

The Pharmazone project is feasible from all perspectives - technical, economic, operational, schedule, and legal. The combination of available technology, minimal costs, market demand, realistic timeline, and clear regulatory path makes this project viable for development and potential commercialization.

---


### 2.1.3 Structured Modeling

Structured modeling uses diagrams to visualize system functionality, data flow, and relationships. These models serve as blueprints for system development.

#### Use Case Diagram

A use case diagram shows the interactions between actors (users) and the system, illustrating what each type of user can do.

**Actors:**
1. **Customer:** End user who purchases medicines and books appointments
2. **Admin:** System administrator who manages the platform
3. **eSewa Gateway:** External payment processing system

**Use Cases:**

**Customer Use Cases:**
- Register Account
- Login/Logout
- Browse Medicines
- Search Medicines
- View Medicine Details
- Add to Cart
- Update Cart
- Remove from Cart
- Checkout
- Make Payment (eSewa/COD)
- Track Order
- Cancel Order
- View Order History
- Download Invoice
- Book Doctor Appointment
- View Appointments
- Cancel Appointment
- Chat with Pharmacist
- View Chat History
- Update Profile

**Admin Use Cases:**
- Login/Logout
- View Dashboard
- Manage Medicines (Add/Edit/Delete)
- Manage Orders
- Update Order Status
- Manage Appointments
- Reschedule Appointments
- View Invoices
- Manage Users
- View Business Analytics

**eSewa Gateway Use Cases:**
- Process Payment
- Send Payment Confirmation
- Handle Payment Failure

**Use Case Specifications:**

**UC-001: User Registration**
- **Actor:** Customer
- **Precondition:** User is not registered
- **Main Flow:**
  1. User navigates to registration page
  2. User enters username, email, password, and user type
  3. System validates input data
  4. System creates user account
  5. System redirects to login page
- **Postcondition:** User account is created
- **Alternative Flow:** If validation fails, system displays error message

**UC-002: Browse and Search Medicines**
- **Actor:** Customer
- **Precondition:** User is on the platform
- **Main Flow:**
  1. User navigates to medicine catalog
  2. System displays list of medicines
  3. User can filter by category or search by name
  4. System displays filtered results
  5. User clicks on medicine to view details
- **Postcondition:** User views medicine information
- **Alternative Flow:** If no results found, system displays "No medicines found"

**UC-003: Place Order**
- **Actor:** Customer
- **Precondition:** User is logged in and has items in cart
- **Main Flow:**
  1. User proceeds to checkout
  2. User enters delivery address
  3. User selects payment method
  4. System calculates total amount
  5. User confirms order
  6. System creates order record
  7. If eSewa selected, redirects to payment gateway
  8. System generates invoice after payment
- **Postcondition:** Order is placed and invoice is generated
- **Alternative Flow:** If payment fails, order remains pending

**UC-004: Book Doctor Appointment**
- **Actor:** Customer
- **Precondition:** User is logged in
- **Main Flow:**
  1. User browses available doctors
  2. User selects a doctor
  3. System displays available time slots
  4. User selects date and time
  5. User fills patient information
  6. User confirms appointment
  7. System creates appointment record
- **Postcondition:** Appointment is booked
- **Alternative Flow:** If time slot is taken, system shows error

**UC-005: Manage Medicine Inventory**
- **Actor:** Admin
- **Precondition:** Admin is logged in
- **Main Flow:**
  1. Admin navigates to medicine management
  2. Admin can add new medicine with details
  3. Admin can edit existing medicine information
  4. Admin can delete medicine
  5. Admin can toggle medicine active status
  6. System updates database
- **Postcondition:** Medicine inventory is updated
- **Alternative Flow:** If validation fails, system shows error

#### Context Diagram

The context diagram shows the Pharmazone system as a single process and its interactions with external entities.

**External Entities:**
1. **Customer:** Interacts with system to purchase medicines and book appointments
2. **Admin:** Manages system operations and business processes
3. **eSewa Payment Gateway:** Processes online payments
4. **Email System:** Sends notifications to users

**Data Flows:**

**From Customer to System:**
- Registration details
- Login credentials
- Medicine search queries
- Cart operations
- Order information
- Payment selection
- Appointment booking details
- Chat messages

**From System to Customer:**
- Medicine catalog
- Search results
- Cart contents
- Order confirmation
- Invoice
- Appointment confirmation
- Chat responses
- Email notifications

**From Admin to System:**
- Login credentials
- Medicine data (add/edit/delete)
- Order status updates
- Appointment management actions
- User management operations

**From System to Admin:**
- Dashboard analytics
- Order list
- Appointment list
- Medicine inventory
- User list
- Business reports

**From System to eSewa Gateway:**
- Payment initiation request
- Transaction details
- Verification request

**From eSewa Gateway to System:**
- Payment confirmation
- Transaction ID
- Payment status

**From System to Email System:**
- Order confirmation emails
- Payment receipts
- Appointment confirmations

#### Data Flow Diagrams (DFD)

Data Flow Diagrams show how data moves through the system at different levels of detail.

**DFD Level 0 (Context Diagram)**

Shows the system as a single process with external entities.

**DFD Level 1 - Main Processes**

The system is decomposed into major processes:

**Process 1.0: User Management**
- Inputs: Registration data, login credentials, profile updates
- Outputs: User account, authentication status, profile information
- Data Stores: User Database
- Description: Handles user registration, authentication, and profile management

**Process 2.0: Medicine Catalog Management**
- Inputs: Search queries, category filters, medicine data (from admin)
- Outputs: Medicine list, medicine details, search results
- Data Stores: Medicine Database, Category Database
- Description: Manages medicine inventory and provides catalog browsing

**Process 3.0: Shopping Cart Management**
- Inputs: Add/remove/update cart items
- Outputs: Cart contents, cart total
- Data Stores: Cart Session Data
- Description: Manages shopping cart operations

**Process 4.0: Order Processing**
- Inputs: Checkout data, delivery address, payment method
- Outputs: Order confirmation, order status, order history
- Data Stores: Order Database, Order Items Database
- Description: Processes orders from checkout to delivery

**Process 5.0: Payment Processing**
- Inputs: Payment method selection, eSewa callback
- Outputs: Payment status, invoice
- Data Stores: Payment Database, Invoice Database
- Description: Handles payment transactions and invoice generation

**Process 6.0: Appointment Management**
- Inputs: Doctor selection, time slot, patient information
- Outputs: Appointment confirmation, appointment list
- Data Stores: Doctor Database, Appointment Database
- Description: Manages doctor appointments and scheduling

**Process 7.0: Pharmacist Chat**
- Inputs: Chat messages, quick response selection
- Outputs: Chat responses, chat history
- Data Stores: Chat Database, Quick Response Database
- Description: Facilitates customer-pharmacist communication

**Process 8.0: Admin Dashboard**
- Inputs: Admin actions, management operations
- Outputs: Business analytics, reports, management interfaces
- Data Stores: All databases
- Description: Provides administrative control and business insights

**DFD Level 2 - User Management (Process 1.0)**

**Process 1.1: User Registration**
- Input: Registration form data
- Output: New user account
- Data Store: User Database
- Description: Validates and creates new user accounts

**Process 1.2: User Authentication**
- Input: Login credentials
- Output: Authentication token, session
- Data Store: User Database
- Description: Verifies user credentials and creates session

**Process 1.3: Profile Management**
- Input: Profile update data
- Output: Updated profile information
- Data Store: User Database, Customer Profile, Pharmacy Profile
- Description: Manages user profile information

**DFD Level 2 - Order Processing (Process 4.0)**

**Process 4.1: Checkout**
- Input: Cart contents, delivery address
- Output: Order draft
- Data Store: Cart Session, Order Database
- Description: Prepares order from cart items

**Process 4.2: Order Creation**
- Input: Order draft, payment method
- Output: Order record with unique order number
- Data Store: Order Database, Order Items Database
- Description: Creates order record in database

**Process 4.3: Order Status Management**
- Input: Status update from admin
- Output: Updated order status
- Data Store: Order Database, Order Status History
- Description: Tracks order status changes

**Process 4.4: Order Tracking**
- Input: Order number
- Output: Order details and status
- Data Store: Order Database
- Description: Provides order tracking information

**DFD Level 2 - Payment Processing (Process 5.0)**

**Process 5.1: Payment Initiation**
- Input: Order details, payment method
- Output: Payment record, eSewa redirect (if applicable)
- Data Store: Payment Database
- Description: Initiates payment process

**Process 5.2: Payment Verification**
- Input: eSewa callback data
- Output: Verified payment status
- Data Store: Payment Database
- Description: Verifies payment transaction authenticity

**Process 5.3: Invoice Generation**
- Input: Completed payment
- Output: PDF invoice
- Data Store: Invoice Database
- Description: Generates professional invoice for completed orders

#### Entity-Relationship (ER) Diagram

The ER diagram shows the database structure and relationships between entities.

**Entities and Attributes:**

**1. User**
- user_id (PK)
- username
- email
- password (hashed)
- user_type (customer/pharmacy/admin)
- phone_number
- date_of_birth
- address
- city
- country
- created_at
- updated_at

**2. CustomerProfile**
- profile_id (PK)
- user_id (FK)
- emergency_contact
- medical_conditions
- preferred_pharmacy_id (FK)

**3. PharmacyProfile**
- profile_id (PK)
- user_id (FK)
- pharmacy_name
- license_number
- gst_number
- description
- website
- is_approved
- rating

**4. Category**
- category_id (PK)
- name
- slug
- description
- image
- is_active
- created_at

**5. Manufacturer**
- manufacturer_id (PK)
- name
- country
- website
- description
- logo

**6. Medicine**
- medicine_id (PK)
- name
- slug
- generic_name
- description
- category_id (FK)
- manufacturer_id (FK)
- prescription_type
- dosage_form
- strength
- pack_size
- composition
- indications
- contraindications
- side_effects
- price
- discount_price
- stock_quantity
- image
- is_active
- is_featured
- created_at
- updated_at

**7. Cart**
- cart_id (PK)
- user_id (FK)
- created_at
- updated_at

**8. CartItem**
- cart_item_id (PK)
- cart_id (FK)
- medicine_id (FK)
- quantity
- added_at

**9. Order**
- order_id (PK)
- order_number (unique)
- user_id (FK)
- status
- payment_status
- payment_method
- subtotal
- tax_amount
- shipping_cost
- discount_amount
- total_amount
- shipping_name
- shipping_address
- shipping_city
- shipping_country
- shipping_phone
- created_at
- updated_at

**10. OrderItem**
- order_item_id (PK)
- order_id (FK)
- medicine_id (FK)
- quantity
- unit_price
- total_price
- medicine_name
- medicine_strength

**11. Payment**
- payment_id (PK)
- payment_id_string (unique)
- order_id (FK)
- user_id (FK)
- amount
- currency
- payment_method
- status
- gateway_transaction_id
- gateway_response
- created_at
- completed_at

**12. Invoice**
- invoice_id (PK)
- invoice_number (unique)
- order_id (FK)
- payment_id (FK)
- status
- subtotal
- tax_amount
- discount_amount
- shipping_amount
- total_amount
- customer_name
- customer_email
- customer_phone
- customer_address
- issue_date
- created_at

**13. Doctor**
- doctor_id (PK)
- user_id (FK)
- full_name
- specialization
- license_number
- qualification
- experience_years
- consultation_fee
- profile_image
- bio
- phone_number
- email
- status
- rating
- created_at

**14. DoctorSchedule**
- schedule_id (PK)
- doctor_id (FK)
- weekday
- start_time
- end_time
- is_active
- created_at

**15. Appointment**
- appointment_id (PK)
- patient_id (FK - User)
- doctor_id (FK)
- appointment_date
- appointment_time
- appointment_type
- duration_minutes
- fee
- status
- patient_age
- patient_gender
- chief_complaint
- symptoms
- medical_history
- doctor_notes
- created_at
- updated_at

**16. AppointmentPayment**
- payment_id (PK)
- appointment_id (FK)
- amount
- payment_method
- payment_status
- transaction_id
- paid_at
- created_at

**17. ChatSession**
- session_id (PK)
- user_id (FK)
- subject
- status
- created_at
- updated_at

**18. ChatMessage**
- message_id (PK)
- session_id (FK)
- sender_type (customer/pharmacist)
- message_text
- created_at

**19. QuickResponse**
- response_id (PK)
- question
- answer
- category
- is_active
- created_at

**Relationships:**

1. **User to CustomerProfile:** One-to-One
2. **User to PharmacyProfile:** One-to-One
3. **User to Cart:** One-to-One
4. **User to Order:** One-to-Many
5. **User to Appointment:** One-to-Many (as patient)
6. **User to Doctor:** One-to-One
7. **User to ChatSession:** One-to-Many
8. **Category to Medicine:** One-to-Many
9. **Manufacturer to Medicine:** One-to-Many
10. **Cart to CartItem:** One-to-Many
11. **Medicine to CartItem:** One-to-Many
12. **Order to OrderItem:** One-to-Many
13. **Medicine to OrderItem:** One-to-Many
14. **Order to Payment:** One-to-One
15. **Order to Invoice:** One-to-One
16. **Payment to Invoice:** One-to-Many
17. **Doctor to DoctorSchedule:** One-to-Many
18. **Doctor to Appointment:** One-to-Many
19. **Appointment to AppointmentPayment:** One-to-One
20. **ChatSession to ChatMessage:** One-to-Many

**Cardinality Notation:**
- 1:1 (One-to-One): Each entity instance relates to exactly one instance of another entity
- 1:N (One-to-Many): One entity instance relates to multiple instances of another entity
- N:M (Many-to-Many): Multiple instances of one entity relate to multiple instances of another entity

---

### 2.1.4 System Requirements Specifications (SRS)

The System Requirements Specification document provides a complete description of the behavior and functionality of the Pharmazone system.

#### Hardware Requirements

**Development Environment:**
- Processor: Intel Core i3 or equivalent (minimum), Intel Core i5 or higher (recommended)
- RAM: 4 GB (minimum), 8 GB or higher (recommended)
- Storage: 10 GB free disk space (minimum), 20 GB (recommended)
- Display: 1366x768 resolution (minimum), 1920x1080 (recommended)
- Internet Connection: Broadband connection for development and testing

**Production Server (for deployment):**
- Processor: 2 vCPU (minimum), 4 vCPU (recommended)
- RAM: 2 GB (minimum), 4 GB or higher (recommended)
- Storage: 20 GB SSD (minimum), 50 GB SSD (recommended)
- Bandwidth: 1 TB/month (minimum), unlimited (recommended)
- Internet Connection: High-speed dedicated connection

**Client Requirements (End Users):**
- Any device with web browser (desktop, laptop, tablet, smartphone)
- Minimum screen resolution: 320px width
- Internet connection: 2 Mbps or higher for optimal experience

#### Software Requirements

**Development Tools:**
- Operating System: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- Python: Version 3.8 or higher
- Django: Version 5.2.7
- Database: SQLite3 (development), PostgreSQL 12+ (production)
- Code Editor: VS Code, PyCharm, or any Python IDE
- Version Control: Git 2.30+
- Web Browser: Chrome, Firefox, Safari, or Edge (latest versions)

**Python Packages:**
- Django 5.2.7
- Pillow (for image handling)
- ReportLab (for PDF generation)
- python-decouple (for environment variables)
- Additional packages as listed in requirements.txt

**Frontend Technologies:**
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5.3
- Font Awesome 6.0
- jQuery 3.6

**Production Server Software:**
- Web Server: Nginx or Apache
- WSGI Server: Gunicorn or uWSGI
- Database: PostgreSQL 12+
- SSL Certificate: Let's Encrypt or commercial SSL
- Email Server: SMTP server for email notifications

**Third-Party Services:**
- eSewa Payment Gateway (test and production credentials)
- Email Service Provider (Gmail SMTP or dedicated email service)

#### Interface Requirements

**User Interface Requirements:**
- Responsive design supporting devices from 320px to 1920px width
- Consistent navigation across all pages
- Clear visual hierarchy and typography
- Accessible color contrast ratios
- Intuitive form layouts with validation feedback
- Loading indicators for asynchronous operations
- Error messages displayed clearly
- Success confirmations for user actions

**Hardware Interface Requirements:**
- Standard keyboard and mouse input
- Touch screen support for mobile devices
- Camera access for prescription image upload (optional)
- Printer support for invoice printing

**Software Interface Requirements:**
- Browser compatibility: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Operating system compatibility: Windows, macOS, Linux, iOS, Android
- Database interface: Django ORM for database operations
- Payment gateway interface: eSewa API integration
- Email interface: SMTP protocol for email sending

**Communication Interface Requirements:**
- HTTP/HTTPS protocol for web communication
- RESTful API principles for data exchange
- JSON format for data serialization
- Secure WebSocket for real-time features (future enhancement)

---

