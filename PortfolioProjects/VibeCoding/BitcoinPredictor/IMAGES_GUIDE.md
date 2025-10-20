# 📸 Image Guide for BitcoinPredictor

## How to Add Images to Your GitHub Repository

### 1. **Images Folder Structure**
```
BitcoinPredictor/
├── images/                     # Screenshots and documentation images
│   ├── app_screenshot.png      # Main app interface
│   ├── data_upload.png         # Data upload page
│   ├── visualization.png       # Charts and graphs
│   ├── model_training.png      # ML model training
│   ├── predictions.png         # Prediction results
│   └── comparison.png          # Model comparison
├── attached_assets/            # Existing data files
│   └── image_*.png            # Your current images
└── README.md
```

### 2. **Adding Images to README.md**

You can reference images in your README.md file like this:

```markdown
## 📸 Screenshots

### Main Dashboard
![BitcoinPredictor Dashboard](images/app_screenshot.png)

### Data Visualization
![Data Charts](images/visualization.png)

### Model Training Interface
![Model Training](images/model_training.png)

### Prediction Results
![Predictions](images/predictions.png)
```

### 3. **Image Best Practices**

- **File Format**: Use PNG for screenshots, JPG for photos
- **Size**: Keep images under 1MB for faster loading
- **Naming**: Use descriptive, lowercase names with hyphens
- **Resolution**: 1080p or 720p for screenshots

### 4. **Current Images Available**
Your project already has some images in `attached_assets/`:
- image_1760386683579.png
- image_1760386707790.png
- image_1760387370912.png
- image_1760387701379.png
- image_1760387965159.png

### 5. **How to Add New Images**

1. **Take Screenshots** of your Streamlit app
2. **Save them** in the `images/` folder
3. **Reference them** in README.md
4. **Commit and push** to GitHub

### 6. **Alternative: Using Existing Images**

You can also move your existing images from `attached_assets/` to `images/` with better names:

```bash
# In your terminal:
cd "C:\Users\tdi-f\Documents\vibe-coding\BitcoinPredictor"
move "attached_assets\image_1760386683579.png" "images\dashboard.png"
move "attached_assets\image_1760386707790.png" "images\data_upload.png"
# ... etc
```

### 7. **GitHub-Specific Image Features**

- **Issues & Pull Requests**: Drag and drop images directly
- **Wiki**: Create detailed documentation with images
- **Releases**: Add screenshots to release notes
- **GitHub Pages**: Host a full website with images

### 8. **Professional Documentation Images**

Consider adding:
- 🏠 **Homepage screenshot**
- 📊 **Key features overview**
- 🔄 **Workflow diagram**
- 📈 **Sample predictions**
- 🎯 **Results comparison**