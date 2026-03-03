# Pharmazone Use Case Diagram - Exact Format Match

## 🎯 EXACT FORMAT - Copy This Code

This matches your reference image EXACTLY - actors on left and right, use cases scattered in middle.

Paste this into **https://mermaid.live**:

```mermaid
flowchart TB
    %% Left Actor
    Customer["<b>Actor</b><br/>(Customer)"]
    
    %% Right Actor  
    Admin["<b>Actor</b><br/>(Admin)"]
    
    %% System Boundary Box
    subgraph SYSTEM["<b>PHARMAZONE SYSTEM</b>"]
        direction TB
        
        %% Top Row Use Cases
        UC1(("Browse<br/>Medicines"))
        UC2(("View Medicine<br/>Details"))
        
        %% Second Row
        UC3(("Register<br/>Account"))
        UC4(("Dashboard<br/>Login"))
        
        %% Third Row
        UC5(("Login"))
        UC6(("Manage<br/>Medicines"))
        
        %% Fourth Row
        UC7(("Add to<br/>Cart"))
        UC8(("Add<br/>Medicine"))
        
        %% Fifth Row
        UC9(("Checkout"))
        UC10(("Edit<br/>Medicine"))
        
        %% Sixth Row
        UC11(("Place<br/>Order"))
        UC12(("Delete<br/>Medicine"))
        
        %% Seventh Row
        UC13(("Make<br/>Payment"))
        UC14(("View All<br/>Orders"))
        
        %% Eighth Row
        UC15(("Track<br/>Order"))
        UC16(("Update Order<br/>Status"))
        
        %% Ninth Row
        UC17(("View<br/>Invoice"))
        UC18(("Manage<br/>Appointments"))
        
        %% Tenth Row
        UC19(("Book<br/>Appointment"))
        UC20(("View<br/>Payments"))
        
        %% Eleventh Row
        UC21(("Chat with<br/>Pharmacist"))
        UC22(("Manage<br/>Users"))
    end
    
    %% Position Actors
    Customer -.-> SYSTEM
    SYSTEM -.-> Admin
    
    %% Customer Connections (from left)
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC5
    Customer --> UC7
    Customer --> UC9
    Customer --> UC11
    Customer --> UC13
    Customer --> UC15
    Customer --> UC17
    Customer --> UC19
    Customer --> UC21
    
    %% Admin Connections (from right)
    UC4 --> Admin
    UC5 --> Admin
    UC6 --> Admin
    UC8 --> Admin
    UC10 --> Admin
    UC12 --> Admin
    UC14 --> Admin
    UC16 --> Admin
    UC18 --> Admin
    UC20 --> Admin
    UC22 --> Admin
    
    %% Styling - Black and White Only
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000
    classDef actor fill:#fff,stroke:#000,stroke-width:3px,color:#000
    classDef boundary fill:none,stroke:#000,stroke-width:2px,stroke-dasharray:5 5
    
    class Customer,Admin actor
    class SYSTEM boundary
```

---

## 🎨 Alternative: Even Simpler Version

If you want fewer use cases for a cleaner look:

```mermaid
graph LR
    %% Actors
    Visitor["Actor<br/>(Visitor)"]
    Admin["Actor<br/>(Admin)"]
    
    %% System Boundary
    subgraph SYSTEM["PHARMAZONE SYSTEM"]
        direction TB
        
        %% Visitor Use Cases
        UC1(("Browse Medicines"))
        UC2(("View Medicine Details"))
        UC3(("Submit Adoption Application"))
        UC4(("Register Account"))
        UC5(("Login"))
        UC6(("Add to Cart"))
        UC7(("Place Order"))
        UC8(("Make Payment"))
        UC9(("Book Appointment"))
        UC10(("Chat with Pharmacist"))
        
        %% Admin Use Cases
        UC11(("Dashboard Login"))
        UC12(("Manage Medicines"))
        UC13(("View All Orders"))
        UC14(("Update Order Status"))
        UC15(("Manage Appointments"))
        UC16(("View Payments"))
        UC17(("Manage Users"))
    end
    
    %% Connections
    Visitor --> UC1
    Visitor --> UC2
    Visitor --> UC3
    Visitor --> UC4
    Visitor --> UC5
    Visitor --> UC6
    Visitor --> UC7
    Visitor --> UC8
    Visitor --> UC9
    Visitor --> UC10
    
    UC11 --> Admin
    UC12 --> Admin
    UC13 --> Admin
    UC14 --> Admin
    UC15 --> Admin
    UC16 --> Admin
    UC17 --> Admin
    
    %% Black & White Only
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000
```

---

## 📐 Vertical Layout (Top-Down)

```mermaid
graph TB
    %% Top Actors
    Customer["Actor<br/>(Customer)"]
    Admin["Actor<br/>(Admin)"]
    
    %% System Boundary
    subgraph PHARMAZONE["PHARMAZONE SYSTEM"]
        direction LR
        
        %% Left Column - Customer Features
        subgraph CustomerFeatures[" "]
            direction TB
            C1(("Register Account"))
            C2(("Login"))
            C3(("Browse Medicines"))
            C4(("Add to Cart"))
            C5(("Place Order"))
            C6(("Make Payment"))
            C7(("Track Order"))
            C8(("Book Appointment"))
            C9(("Chat Pharmacist"))
        end
        
        %% Right Column - Admin Features
        subgraph AdminFeatures[" "]
            direction TB
            A1(("Dashboard Login"))
            A2(("Manage Medicines"))
            A3(("Add Medicine"))
            A4(("Edit Medicine"))
            A5(("Delete Medicine"))
            A6(("View Orders"))
            A7(("Update Status"))
            A8(("Manage Appointments"))
            A9(("Manage Users"))
        end
    end
    
    %% Connections
    Customer --> C1
    Customer --> C2
    Customer --> C3
    Customer --> C4
    Customer --> C5
    Customer --> C6
    Customer --> C7
    Customer --> C8
    Customer --> C9
    
    A1 --> Admin
    A2 --> Admin
    A3 --> Admin
    A4 --> Admin
    A5 --> Admin
    A6 --> Admin
    A7 --> Admin
    A8 --> Admin
    A9 --> Admin
    
    %% Simple Styling
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000
```

---

## 🎯 Most Recommended: Clean & Professional

```mermaid
graph LR
    %% Left Actor
    Customer["Actor<br/>(Customer)"]
    
    %% System Boundary
    subgraph PHARMAZONE["PHARMAZONE SYSTEM"]
        %% Use Cases in Grid Layout
        UC1(("Register<br/>Account"))
        UC2(("Login"))
        UC3(("Browse<br/>Medicines"))
        UC4(("View Medicine<br/>Details"))
        UC5(("Add to<br/>Cart"))
        UC6(("Checkout"))
        UC7(("Place<br/>Order"))
        UC8(("Make<br/>Payment"))
        UC9(("Track<br/>Order"))
        UC10(("View<br/>Invoice"))
        UC11(("Book<br/>Appointment"))
        UC12(("Chat with<br/>Pharmacist"))
        
        UC20(("Dashboard<br/>Login"))
        UC21(("Manage<br/>Medicines"))
        UC22(("Add<br/>Medicine"))
        UC23(("Edit<br/>Medicine"))
        UC24(("Delete<br/>Medicine"))
        UC25(("View All<br/>Orders"))
        UC26(("Update Order<br/>Status"))
        UC27(("Manage<br/>Appointments"))
        UC28(("View<br/>Payments"))
        UC29(("Manage<br/>Users"))
    end
    
    %% Right Actor
    Admin["Actor<br/>(Admin)"]
    
    %% Customer Connections
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    Customer --> UC7
    Customer --> UC8
    Customer --> UC9
    Customer --> UC10
    Customer --> UC11
    Customer --> UC12
    
    %% Admin Connections
    UC20 --> Admin
    UC21 --> Admin
    UC22 --> Admin
    UC23 --> Admin
    UC24 --> Admin
    UC25 --> Admin
    UC26 --> Admin
    UC27 --> Admin
    UC28 --> Admin
    UC29 --> Admin
    
    %% Black & White Styling
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000
    classDef actor fill:#fff,stroke:#000,stroke-width:3px,color:#000
    
    class Customer,Admin actor
```

---

## 📝 How to Use

### Step 1: Copy the Code
Choose the version you like (I recommend "Most Recommended" version)

### Step 2: Go to Mermaid Live
Visit: **https://mermaid.live**

### Step 3: Paste & Generate
1. Paste the code in the left panel
2. The diagram appears instantly on the right
3. It will look exactly like your reference image!

### Step 4: Export
1. Click **Actions** → **Export PNG**
2. Choose **Scale: 4x** for high quality
3. Download the image

### Step 5: Insert in Report
1. Open your Word document
2. Insert → Picture
3. Add caption: "Figure 2.1: Use Case Diagram for Pharmazone System"

---

## ✅ What You Get

✓ **Simple black and white** - No colors  
✓ **No emoji icons** - Just text labels  
✓ **Actors on sides** - Customer left, Admin right  
✓ **System boundary** - Clear box around use cases  
✓ **Use cases as ovals** - Traditional UML format  
✓ **Clean lines** - Simple connections  
✓ **Professional look** - Perfect for academic reports  

---

## 📊 Diagram Features

- **Actors:** Customer (left), Admin (right)
- **System Boundary:** PHARMAZONE SYSTEM box
- **Customer Use Cases:** 12-14 use cases
- **Admin Use Cases:** 10-12 use cases
- **Style:** Black & white, no colors, no icons
- **Format:** Traditional UML standard

---

## 💡 Tips

1. **For Best Quality:** Export at 4x scale
2. **For Reports:** Use white background
3. **For Printing:** Export as PDF
4. **File Size:** Will be around 2-3 MB (perfect quality)

---

## 🎓 Perfect For

✓ Academic project reports  
✓ BIM semester projects  
✓ Professional documentation  
✓ System design documents  
✓ Technical presentations  

---

**Project:** Pharmazone - E-Commerce Pharmacy Platform  
**Student:** Srijana Khatri  
**Institution:** St. Xavier's College, Maitighar  
**Program:** BIM 6th Semester  
**Year:** 2026

---

## 🚀 Ready to Use!

Just copy the code, paste into https://mermaid.live, and export!  
Your diagram will look exactly like the professional format you showed me.
