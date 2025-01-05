# Course Recommendation System

## **Introduction**
The Course Recommendation System leverages machine learning to provide personalized course recommendations based on the user's input, such as:
- **Area of Interest**
- **Career Goal**
- **Preferred Learning Style**

It enhances user experience by offering:
- **Course Descriptions**
- **VR/AR Preview Links**
- **Course Introduction Videos**

![Screenshot from 2025-01-05 12-59-42](https://github.com/user-attachments/assets/e8f10dd3-642b-4cd8-ab4f-ea0b877ffdcd)
---

## **System Flowchart**
Below is a Mermaid diagram illustrating the system’s workflow:

```mermaid
flowchart TD
    A[User Opens Web Application] --> B{Did User Select All Fields?}
    B -- No --> C[Prompt User to Complete All Fields]
    B -- Yes --> D[Send Request to Backend]
    D --> E[Flask Backend Receives Input]
    E --> F[Preprocess User Input and Encode Features]
    F --> G[Predict Recommended Course]
    G --> H{Course Exists in Metadata?}
    H -- Yes --> I[Send Course Details: Description, VR Link, Video Link]
    H -- No --> J[Send Default Message: No Immersive Preview Available]
    I --> K[Display Course Details on Frontend]
    J --> K

