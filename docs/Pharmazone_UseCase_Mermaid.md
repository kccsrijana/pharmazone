# Pharmazone Use Case Diagram - Mermaid Code

## 🎨 Mermaid Diagram Code

Copy and paste this code into any Mermaid-compatible editor:
- GitHub Markdown files
- Mermaid Live Editor: https://mermaid.live
- VS Code with Mermaid extension
- GitLab, Notion, Obsidian, etc.

---

## 📊 Full Use Case Diagram

```mermaid
graph TB
    subgraph PHARMAZONE_SYSTEM["PHARMAZONE SYSTEM"]
        %% Customer Use Cases
        UC1((Register Account))
        UC2((Login))
        UC3((Browse Medicines))
        UC4((Search Medicines))
        UC5((View Medicine Details))
        UC6((Add to Cart))
        UC7((Update Cart))
        UC8((Checkout))
        UC9((Place Order))
        UC10((Track Order))
        UC11((Make Payment))
        UC12((View Invoice))
        UC13((Book Appointment))
        UC14((Chat with Pharmacist))
        UC15((Cancel Order))
        
        %% Admin Use Cases
        UC16((View Dashboard))
        UC17((Manage Medicines))
        UC18((Add Medicine))
        UC19((Edit Medicine))
        UC20((Delete Medicine))
        UC21((View All Orders))
        UC22((Update Order Status))
        UC23((Process Order))
        UC24((Manage Appointments))
        UC25((View Payments))
        UC26((Process Refund))
        UC27((Generate Invoice))
        UC28((Manage Users))
        UC29((Update Stock))
        UC30((View Statistics))
    end
    
    %% Actors
    Customer[👤 Customer]
    Admin[👨‍💼 Admin]
    
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
    Customer --> UC13
    Customer --> UC14
    Customer --> UC15
    
    %% Admin Connections
    Admin --> UC2
    Admin --> UC16
    Admin --> UC17
    Admin --> UC18
    Admin --> UC19
    Admin --> UC20
    Admin --> UC21
    Admin --> UC22
    Admin --> UC23
    Admin --> UC24
    Admin --> UC25
    Admin --> UC26
    Admin --> UC27
    Admin --> UC28
    Admin --> UC29
    Admin --> UC30
    
    %% Styling
    classDef customerUC fill:#d5e8d4,stroke:#82b366,stroke-width:2px
    classDef adminUC fill:#ffe6cc,stroke:#d79b00,stroke-width:2px
    classDef actor fill:#dae8fc,stroke:#6c8ebf,stroke-width:3px
    
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10,UC11,UC12,UC13,UC14,UC15 customerUC
    class UC16,UC17,UC18,UC19,UC20,UC21,UC22,UC23,UC24,UC25,UC26,UC27,UC28,UC29,UC30 adminUC
    class Customer,Admin actor
```

---

## 🎯 Simplified Version (Fewer Use Cases)

If you want a cleaner diagram with main features only:

```mermaid
graph LR
    subgraph PHARMAZONE["PHARMAZONE SYSTEM"]
        %% Customer Use Cases
        UC1((Register))
        UC2((Login))
        UC3((Browse Medicines))
        UC4((Add to Cart))
        UC5((Place Order))
        UC6((Make Payment))
        UC7((Track Order))
        UC8((Book Appointment))
        UC9((Chat Pharmacist))
        
        %% Admin Use Cases
        UC10((Dashboard))
        UC11((Manage Medicines))
        UC12((Manage Orders))
        UC13((Manage Appointments))
        UC14((View Payments))
        UC15((Manage Users))
    end
    
    Customer[👤 Customer] --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    Customer --> UC7
    Customer --> UC8
    Customer --> UC9
    
    Admin[👨‍💼 Admin] --> UC2
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC13
    Admin --> UC14
    Admin --> UC15
    
    classDef customerStyle fill:#d5e8d4,stroke:#82b366,stroke-width:2px
    classDef adminStyle fill:#ffe6cc,stroke:#d79b00,stroke-width:2px
    
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9 customerStyle
    class UC10,UC11,UC12,UC13,UC14,UC15 adminStyle
```

---

## 🔄 Alternative Layout (Left-Right)

```mermaid
graph LR
    Customer[👤<br/>Customer]
    
    subgraph System["PHARMAZONE SYSTEM"]
        direction TB
        subgraph CustomerFeatures["Customer Features"]
            UC1((Register))
            UC2((Login))
            UC3((Browse<br/>Medicines))
            UC4((Shopping<br/>Cart))
            UC5((Place<br/>Order))
            UC6((Payment))
            UC7((Appointments))
            UC8((Chat))
        end
        
        subgraph AdminFeatures["Admin Features"]
            UC10((Dashboard))
            UC11((Manage<br/>Medicines))
            UC12((Manage<br/>Orders))
            UC13((Manage<br/>Appointments))
            UC14((Payments))
            UC15((Users))
        end
    end
    
    Admin[👨‍💼<br/>Admin]
    
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    Customer --> UC7
    Customer --> UC8
    
    Admin --> UC2
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC13
    Admin --> UC14
    Admin --> UC15
    
    classDef green fill:#d5e8d4,stroke:#82b366
    classDef orange fill:#ffe6cc,stroke:#d79b00
    
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8 green
    class UC10,UC11,UC12,UC13,UC14,UC15 orange
```

---

## 📱 Vertical Layout (Top-Down)

```mermaid
graph TD
    Customer[👤 Customer]
    Admin[👨‍💼 Admin]
    
    Customer --> System
    Admin --> System
    
    subgraph System["PHARMAZONE SYSTEM"]
        direction LR
        
        subgraph Auth["Authentication"]
            A1((Register))
            A2((Login))
        end
        
        subgraph Shopping["Shopping"]
            S1((Browse))
            S2((Cart))
            S3((Checkout))
            S4((Order))
        end
        
        subgraph Healthcare["Healthcare"]
            H1((Appointments))
            H2((Chat))
        end
        
        subgraph AdminPanel["Admin Panel"]
            AD1((Dashboard))
            AD2((Medicines))
            AD3((Orders))
            AD4((Users))
        end
    end
    
    classDef authStyle fill:#e1d5e7,stroke:#9673a6
    classDef shopStyle fill:#d5e8d4,stroke:#82b366
    classDef healthStyle fill:#f8cecc,stroke:#b85450
    classDef adminStyle fill:#ffe6cc,stroke:#d79b00
    
    class A1,A2 authStyle
    class S1,S2,S3,S4 shopStyle
    class H1,H2 healthStyle
    class AD1,AD2,AD3,AD4 adminStyle
```

---

## 🎨 With Include/Extend Relationships

```mermaid
graph TB
    Customer[👤 Customer]
    Admin[👨‍💼 Admin]
    
    subgraph PHARMAZONE["PHARMAZONE SYSTEM"]
        UC1((Login))
        UC2((Browse<br/>Medicines))
        UC3((Add to<br/>Cart))
        UC4((Checkout))
        UC5((Place<br/>Order))
        UC6((Make<br/>Payment))
        UC7((Send Email<br/>Notification))
        UC8((Generate<br/>Invoice))
        
        UC10((Manage<br/>Medicines))
        UC11((Manage<br/>Orders))
        UC12((Dashboard))
    end
    
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    
    Admin --> UC1
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    
    UC5 -.->|includes| UC6
    UC6 -.->|extends| UC7
    UC6 -.->|includes| UC8
    
    classDef customer fill:#d5e8d4,stroke:#82b366
    classDef admin fill:#ffe6cc,stroke:#d79b00
    classDef system fill:#dae8fc,stroke:#6c8ebf
    
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8 customer
    class UC10,UC11,UC12 admin
```

---

## 🌐 How to Use This Code

### Option 1: GitHub/GitLab
1. Create or edit a `.md` file
2. Paste the mermaid code block
3. Commit and view - it will render automatically!

### Option 2: Mermaid Live Editor
1. Go to https://mermaid.live
2. Paste the code in the left panel
3. See the diagram on the right
4. Export as PNG, SVG, or PDF

### Option 3: VS Code
1. Install "Markdown Preview Mermaid Support" extension
2. Create a `.md` file with the mermaid code
3. Open preview (Ctrl+Shift+V)
4. Right-click diagram → Save as image

### Option 4: Notion
1. Type `/code`
2. Select "Mermaid" as language
3. Paste the code
4. Notion will render it automatically

### Option 5: Obsidian
1. Create a note
2. Add mermaid code block
3. Switch to preview mode
4. Diagram renders automatically

---

## 📸 Export Options

### From Mermaid Live Editor:
1. **PNG** - For Word documents, reports
2. **SVG** - For scalable vector graphics
3. **PDF** - For printing
4. **Markdown** - To embed in documentation

### Quality Settings:
- Use **PNG** with high DPI for reports
- Use **SVG** for presentations (scales perfectly)
- Use **PDF** for printing

---

## 🎯 Customization Tips

### Change Colors:
```mermaid
classDef myStyle fill:#your-color,stroke:#border-color,stroke-width:2px
class UC1,UC2 myStyle
```

### Change Shape:
- `(( ))` = Circle (use case)
- `[ ]` = Rectangle (actor)
- `[( )]` = Stadium shape
- `{ }` = Diamond
- `[[ ]]` = Subroutine

### Change Arrow Style:
- `-->` = Solid arrow
- `-.->` = Dashed arrow (for include/extend)
- `==>` = Thick arrow
- `--x` = Arrow with cross

### Add Labels:
```mermaid
Customer -->|uses| UC1
UC1 -.->|includes| UC2
```

---

## ✅ Advantages of Mermaid

1. **Version Control** - Text-based, works with Git
2. **Easy to Edit** - Just edit text, no special tools needed
3. **Auto-Rendering** - GitHub, GitLab, Notion render automatically
4. **Consistent Style** - Programmatic styling
5. **Export Options** - PNG, SVG, PDF
6. **Collaboration** - Easy to review and merge changes
7. **Documentation** - Lives with your code

---

## 📚 Resources

- **Mermaid Documentation:** https://mermaid.js.org
- **Live Editor:** https://mermaid.live
- **GitHub Guide:** https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/
- **Syntax Guide:** https://mermaid.js.org/syntax/flowchart.html

---

**Project:** Pharmazone - E-Commerce Pharmacy Platform  
**Student:** Srijana Khatri  
**Institution:** St. Xavier's College, Maitighar  
**Program:** BIM 6th Semester  
**Year:** 2026
