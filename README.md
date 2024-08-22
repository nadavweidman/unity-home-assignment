# unity-home-assignment
# Project Overview

This project consists of a microservices-based architecture with the following components:

- **MongoDB**: Used for storing user purchases.
- **Kafka**: A distributed messaging system for handling event-driven communication.
- **Customer Management API**: A backend API that interacts with MongoDB to manage customer purchase data.
- **Customer Facing Web Server**: A frontend service that handles customer-facing operations, including purchase requests and retrieving purchase history.

## Architecture

The architecture is built using Kubernetes and is deployed on an Amazon EKS cluster. The components are packaged and deployed using Helm charts.

### Components

1. **MongoDB**: 
   - Stores customer purchase records.
   - Deployed as a Helm dependency.

2. **Kafka**:
   - Handles event-driven communication.
   - Deployed as a Helm dependency.

3. **Customer Management API**:
   - Provides endpoints to interact with MongoDB and manage customer purchases.
   - Exposes APIs for internal communication.
   - Deployed as a Helm dependency (a helm chart which i created).

4. **Customer Facing Web Server**:
   - Provides a web interface for customers to make purchases and view their purchase history.
   - Interacts with the Customer Management API and Kafka.
   - Deployed as a Helm dependency (a helm chart which i created).

### Helm Charts

- **Parent Helm Chart**:
  - This chart encapsulates the entire application, managing the deployment of all components (MongoDB, Kafka, API, and Web Server) as dependencies.
  
- **Helm Dependencies**:
  - The parent Helm chart references the individual charts for MongoDB, Kafka, API, and Web Server, ensuring all components are deployed and configured correctly.

### Deployment

1. **Deploying the Application**:
   - Clone the repository.
   - Navigate to the Parent Helm chart directory (unity-home-assignment-chart).
   - Deploy the parent Helm chart using:
     ```bash
     helm install unity-home-assignment .
     ```
    

2. **Accessing the Web Server**:
   - After deployment, retrieve the external IP address of the LoadBalancer service associated with the Customer Facing Web Server:
     ```bash
     kubectl get svc
     ```
   - Access the web server using the external IP on port `8080`.

### Operations

- **Buy a Product**:
  - Endpoint: `/api/buy/`
  - Method: `POST`
  - Request Body:
    ```json
    {
        "username": "<username>",
        "userId": "<userId>",
        "price": "<price>"
    }
    ```
  - Sends a purchase request that is handled by Kafka and stored in MongoDB.

- **Get All Purchases**:
  - Endpoint: `/api/getAllUserBuys/`
  - Method: `GET`
  - Retrieves all purchase records from the Customer Management API.