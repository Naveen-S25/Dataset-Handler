# 🛡️ Dataset Handler Pro
**A Professional Enterprise-Grade Data Quality & Cleaning Toolkit**

Dataset Handler is a high-performance Streamlit application designed for data analysts to audit, clean, and validate large datasets. It features a sophisticated Deep Blue UI, real-time health metrics, and an intelligent "Guard" system to catch statistical anomalies.

---

## 🚀 Key Features

### 📊 1. Intelligent Quality Dashboard
- **Health Scoring:** Automatically calculates a data integrity percentage based on null values and duplicates.
- **Statistical Outlier Detection:** Uses Z-Score analysis to highlight anomalies in red ($|Z| > 3$).
- **Live Search:** High-speed filtering to find specific keywords across thousands of rows.

### 🛠️ 2. Smart Cleaning Toolkit
- **Memory Engine:** Features **Undo** and **Reset** capabilities to ensure a safe cleaning workflow.
- **Bulk Operations:** One-click solutions for filling missing values, dropping duplicates, and text normalization.
- **Schema Validator:** Ensures your data types (Numeric vs String) match business requirements.

### 💻 3. Professional SQL Console
- Allows power users to write **SQL-style queries** (e.g., `Amount > 500 and Status == 'Shipped'`) to filter datasets with precision.

### 🧠 4. AI-Powered Audit
- Connects to **OpenRouter (Gemini/DeepSeek)** to generate a human-readable summary of data issues and suggest strategic improvements.

### 📜 5. Audit Trail
- Maintains a transparent **Activity Log** of every modification made, ensuring data lineage and accountability.

---

## 🛠️ Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/dataset-handler.git](https://github.com/YOUR_USERNAME/dataset-handler.git)
