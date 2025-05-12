
#Detailed explanation of the operation and use of the hospital management APP project
##Project Operation Guide
### 1. Environmental preparation
####Development environment requirements:
-* * Operating System * *: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+recommended)
-Node. js: v14. x or higher version
-* * npm * *: v6. x or higher version (or using yarn)
-MongoDB: Community Version 4.4+
-Mobile Development Environment:
-Android development: Android Studio+Android SDK
-IOS development: Xcode 12+
####Tool installation:
```bash
#Check if Node.js is installed
node -v
npm -v
#If not installed, download and install from the official website:
#  https://nodejs.org/
#MongoDB Installation Guide:
#  https://docs.mongodb.com/manual/installation/
```
### 2. Project acquisition and initialization
```bash
#Clone project repository
git clone  https://github.com/yazdanhaider/Hospital-Management.git
#Enter the project directory
cd Hospital-Management
#Install backend dependencies
cd server
npm install
#Install front-end dependencies
cd ../client
npm install
```
### 3. Database Configuration
1. Start MongoDB service:
```bash
mongod
```
(Windows users may need to run with administrator privileges)
2. Create a database and initial data:
```bash
cd server
npm run seed
```
This will create:
-An administrator account (admin/admin123)
-Several testing doctor accounts
-Basic department settings
-Initial drug inventory
### 4. Configure environment variables
Create an. env file in the 'server' directory:
```env
PORT=5000
MONGODB_URI= mongodb://localhost:27017/hospital_management
JWT_SECRET=your_strong_secret_key_here
NODE_ENV=development
```
### 5. startup project
####Start backend service:
```bash
cd server
npm start
```
After successful startup, the console will display:
```
Server is running on port 5000
MongoDB Connected...
```
####Launch front-end application:
**Method 1: Use a simulator**
```bash
cd client
Npm run Android # or npm run iOS
```
**Method 2: Development Mode**
```bash
cd client
npm start
```
Then open the Expo development tool in the browser, or use the Expo Go app to scan the QR code
### 6. Test account
-Administrator: admin/admin123
-Doctor: doctor1/doctor123
-Patient: Patient1/Patient123
##Project Architecture Analysis
###Front end structure (client/)
```
src/
∝ - Assets/# Static Resources
∝ - Components/# Reusable Components
∝ - Navigation/# Routing Configuration
∝ - screens/# Each functional page
∝ - Services/# API Services
∝ - Store/# Redux Status Management
∝ - Utilities/# utility functions
└ -- App. js # Main Entry File
```
###Backend structure (server/)
```
src/
∝ - config/# configuration file
∝ - controllers/# business logic
∝ - models/# database models
∝ - routes/# API routes
∝ - middleware/# middleware
∝ - Utilities/# utility functions
└ - Server. js # Main Entry File
```
##Core Function Usage Instructions
### 1. Patient management process
**Patient registration:**
1. Open the app and select "Register"
2. Fill in the basic information (name, mobile phone number, ID number, etc.)
3. Set login password
4. After completing the verification, log in to the system
**Appointment registration:**
1. After logging in, click on "Appointment Registration"
2. Choose a department (such as internal medicine, surgery)
3. Select a doctor (display doctor profile and scheduling time)
4. Select an available time period
5. Confirm the appointment and pay the registration fee
### 2. Doctor workflow
**Reception of patients:**
1. Log in to the doctor's account
2. View the "Today's Schedule" list
3. Select patients who have already checked in
4. View the patient's medical history
5. Enter diagnostic information and prescription
**Prescription issuance:**
1. Click on "Prescription" on the diagnostic page
2. Search for drug names
3. Set usage and dosage
4. Add medical advice instructions
5. Submit prescription (automatic deduction of inventory)
### 3. Administrator function
**User management:**
1. Log in to the administrator account
2. Go to "System Management">"User Management"
3. User accounts can be added/edited/disabled
4. Set up user roles (doctors, nurses, pharmacists, etc.)
**Drug inventory management:**
1. Enter "Pharmacy Management"
2. View current inventory and alert drugs
3. Click on "Stock in" to add new drugs
4. Set drug information (name, specifications, price, etc.)
5. Set inventory warning threshold
##API interface documentation
The backend provides RESTful APIs, with the main endpoints including:
|Endpoint | Me

