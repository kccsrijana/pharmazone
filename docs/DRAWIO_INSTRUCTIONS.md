# 📐 How to Use the Pharmazone Use Case Diagram in Draw.io

## 🎯 Quick Start

### Step 1: Open Draw.io
1. Go to **https://app.diagrams.net** (or https://draw.io)
2. Or download the desktop app from https://github.com/jgraph/drawio-desktop/releases

### Step 2: Import the Diagram
1. Click **File** → **Open from** → **Device**
2. Navigate to your project folder: `docs/Pharmazone_UseCase_Diagram.drawio`
3. Select the file and click **Open**

### Step 3: View and Edit
- The diagram will open with all actors, use cases, and connections
- You can now edit, customize, and export the diagram

---

## 📊 What's Included in the Diagram

### Actors (4):
- **Customer** (Green) - Left side
- **Admin** (Orange) - Right side
- **eSewa Gateway** (Red) - Bottom
- **Email System** (Yellow) - Top

### Use Cases (40+):
- **Customer Use Cases** (Green ellipses):
  - Authentication: Register, Login, Update Profile
  - Shopping: Browse, Search, View Details, Cart Management
  - Orders: Checkout, Place Order, Track, Cancel
  - Invoices: View, Download
  - Healthcare: Browse Doctors, Book Appointments, Chat with Pharmacist

- **Admin Use Cases** (Orange ellipses):
  - Dashboard & Statistics
  - Medicine Management: Add, Edit, Delete, Update Stock
  - Order Management: View, Update Status, Process
  - Appointment Management
  - Payment & Invoice Management
  - User Management

- **Payment Use Cases** (Red ellipses):
  - Make Payment (eSewa)
  - Make Payment (COD)
  - Process Payment

- **Notification Use Cases** (Yellow ellipses):
  - Send Order Confirmation
  - Send Payment Receipt
  - Send Appointment Confirmation

### Relationships:
- **Solid lines** = Association (Actor uses Use Case)
- **Dashed lines** = Include/Extend relationships

---

## 🎨 Customization Options

### Change Colors:
1. Select a use case ellipse
2. Click the **Fill Color** button in the toolbar
3. Choose your preferred color

### Resize Elements:
1. Click on any element
2. Drag the corner handles to resize
3. Hold **Shift** while dragging to maintain proportions

### Add More Use Cases:
1. Click **+** button or press **Ctrl+K** (Cmd+K on Mac)
2. Search for "ellipse" in the shapes panel
3. Drag an ellipse onto the canvas
4. Double-click to add text

### Add Connections:
1. Hover over an actor or use case
2. Click and drag from the blue arrow that appears
3. Drop on the target element
4. The connection will be created automatically

### Change Layout:
1. Select multiple elements (Ctrl+Click or drag to select)
2. Use **Arrange** menu to align, distribute, or group elements
3. Use **Format** → **Spacing** to adjust gaps

---

## 💾 Export Options

### Export as PNG (for Word/PDF):
1. Click **File** → **Export as** → **PNG**
2. Settings:
   - **Zoom:** 100% (or higher for better quality)
   - **Border Width:** 10
   - **Transparent Background:** Unchecked (white background)
3. Click **Export**
4. Save the file
5. Insert into your Word document or report

### Export as PDF:
1. Click **File** → **Export as** → **PDF**
2. Settings:
   - **Page View:** Fit to 1 page
   - **Crop:** Checked
3. Click **Export**
4. Save the PDF file

### Export as SVG (Vector - Best Quality):
1. Click **File** → **Export as** → **SVG**
2. Keep default settings
3. Click **Export**
4. SVG files can be inserted into Word and maintain quality at any size

### Print:
1. Click **File** → **Print**
2. Adjust print settings
3. Select **Save as PDF** or print directly

---

## 🔧 Advanced Editing

### Add System Boundary:
The diagram already has a system boundary (the large blue rectangle).
To modify it:
1. Click on the boundary
2. Resize by dragging corners
3. Change color in **Format** panel
4. Edit title by double-clicking

### Add Include/Extend Relationships:
1. Draw a connection between two use cases
2. Right-click the connection
3. Select **Edit Style**
4. Add: `dashed=1;endArrow=open;endFill=0;`
5. Add label: Right-click → **Edit Label** → Type "<<include>>" or "<<extend>>"

### Group Related Use Cases:
1. Select multiple use cases (Ctrl+Click)
2. Right-click → **Group** (or press Ctrl+G)
3. Now they move together as one unit

### Add Notes/Comments:
1. Click **+** → Search for "note" or "text box"
2. Drag onto canvas
3. Add your notes
4. Use for explanations or legends

---

## 📱 Tips for Best Results

### For Project Reports:
1. Export as **PNG** with **200% zoom** for high quality
2. Use **white background** (not transparent)
3. Add **10-20px border** for clean edges
4. Save as: `Pharmazone_UseCase_Diagram.png`

### For Presentations:
1. Export as **SVG** for scalability
2. Or export as **PNG** with **300% zoom**
3. Use **transparent background** if needed

### For Printing:
1. Use **File** → **Page Setup** to set paper size (A4 or Letter)
2. Adjust diagram to fit one page
3. Export as **PDF** for best print quality

---

## 🎯 Quick Keyboard Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| New Shape | Ctrl+K | Cmd+K |
| Delete | Delete | Delete |
| Duplicate | Ctrl+D | Cmd+D |
| Group | Ctrl+G | Cmd+G |
| Ungroup | Ctrl+Shift+U | Cmd+Shift+U |
| Undo | Ctrl+Z | Cmd+Z |
| Redo | Ctrl+Y | Cmd+Y |
| Select All | Ctrl+A | Cmd+A |
| Zoom In | Ctrl++ | Cmd++ |
| Zoom Out | Ctrl+- | Cmd+- |
| Fit to Page | Ctrl+Shift+F | Cmd+Shift+F |

---

## 🔍 Troubleshooting

### Problem: Diagram looks too small
**Solution:** 
- Click **View** → **Zoom** → **Fit**
- Or use **Ctrl+Shift+F** to fit to window

### Problem: Can't see all elements
**Solution:**
- Click **View** → **Outline** to see thumbnail
- Use scroll bars or zoom out

### Problem: Connections look messy
**Solution:**
- Right-click connection → **Edit Style**
- Change routing: `curved=1;` or `orthogonal=1;`
- Or manually adjust waypoints by dragging

### Problem: Export is low quality
**Solution:**
- Increase zoom percentage when exporting
- Use 200-300% for high-quality images
- Or export as SVG for vector graphics

### Problem: File won't open
**Solution:**
- Make sure you're using Draw.io (diagrams.net)
- Try opening in browser version: https://app.diagrams.net
- Check file isn't corrupted (should be ~50KB)

---

## 📚 Additional Resources

### Draw.io Documentation:
- Official Guide: https://www.diagrams.net/doc/
- Video Tutorials: https://www.youtube.com/c/drawio
- UML Shapes: https://www.diagrams.net/blog/uml-diagrams

### UML Use Case Diagram Standards:
- Use ellipses for use cases
- Use stick figures for actors
- Use solid lines for associations
- Use dashed lines with <<include>> or <<extend>> for relationships
- Use rectangles for system boundaries

---

## ✅ Checklist for Your Report

- [ ] Open the diagram in Draw.io
- [ ] Review all use cases and actors
- [ ] Customize colors if needed (optional)
- [ ] Add any missing use cases specific to your implementation
- [ ] Export as PNG (200% zoom, white background)
- [ ] Save as: `Pharmazone_UseCase_Diagram.png`
- [ ] Insert into your project report
- [ ] Add caption: "Figure X: Use Case Diagram for Pharmazone System"
- [ ] Reference the diagram in your text

---

## 🎨 Color Scheme Used

- **Customer Use Cases:** Light Green (#d5e8d4)
- **Admin Use Cases:** Light Orange (#ffe6cc)
- **Payment Use Cases:** Light Red (#f8cecc)
- **Healthcare Use Cases:** Light Purple (#e1d5e7)
- **Notification Use Cases:** Light Yellow (#fff2cc)
- **System Boundary:** Light Blue (#dae8fc)

---

## 📞 Need Help?

If you encounter any issues:
1. Check the Draw.io documentation
2. Watch tutorial videos on YouTube
3. Try the browser version if desktop app has issues
4. Export and re-import if diagram seems corrupted

---

**Created for:** Pharmazone E-Commerce Pharmacy Platform  
**Student:** Srijana Khatri  
**Institution:** St. Xavier's College, Maitighar  
**Program:** BIM 6th Semester  
**Year:** 2026

---

Good luck with your project report! 🎓
