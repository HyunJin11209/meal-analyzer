## Project Overview

Meal Analyzer is a web application that analyzes total calorie intake and macronutrient ratios (carbohydrates, protein, and fat) based on the user's meal input.  
When users enter food items in natural language, the NLP model recognizes the text and retrieves nutritional information from the built-in nutrition database to calculate the values automatically.

Additionally, the service incorporates the **recommended dietary intake standards (KDRIs) for men and women aged 19–29**, allowing users to select their gender for more accurate and personalized comparison results.  
This enables the application to go beyond simple nutrient calculation and provide user-specific insights and dietary guidance.

Built with Streamlit, the project enables rapid prototyping without the need for separate UI development.  
Users can easily view **total calories, nutrient distribution, simple feedback, and comparison results against recommended intake values** through a clean and intuitive interface.

In short, **just enter what you ate and select your gender — the AI will analyze your nutrition and compare it to the standard recommended intake.**

## Example Output

<img width="601" height="812" alt="image" src="https://github.com/user-attachments/assets/f9ed2f8a-a3a4-4e95-b633-79ab641dbb68" />

##  Dependencies & Versions

The following packages were used to run this project:

| Package | Version |
|--------|---------|
| Python | 3.9+ |
| Streamlit | 1.50.0 |
| Pandas | 2.3.3 |
| NumPy | 2.0.2 |
| Scikit-learn | 1.6.1 |
| Transformers | 4.57.3 |

> All dependencies can be installed using the command below (based on `requirements.txt`):

```bash
python -m pip install -r requirements.txt
```

## How to Run

1. Clone the repository
```bash
git clone https://github.com/HyunJin11209/meal-analyzer.git
cd meal-analyzer
```
2. Install required packages
```bash
python -m pip install -r requirements.txt
```
3. Run the application
```bash
python -m streamlit run src/app.py
```
Once executed, the browser will open automatically.
You can also access the application manually at:

🔗 http://localhost:8501

## References

1. Streamlit Documentation
https://docs.streamlit.io/

2. Hugging Face Transformers Documentation
https://huggingface.co/docs/transformers

3. Kim, Jung-Hyun., Lee, Min-Jun., Kim, Jung-Yeon., Park, Yu-Kyung., & Park, Eun-Ju.
Easy Nutrition (3rd Edition). Soohaksa Publishing, 2011.
→ The recommended calorie and intake values used in this project are based on the
2020 Korean Dietary Reference Intakes (KDRIs) included in this textbook.


##  Team Members & Roles

202334524 인공지능학과 이충현
- create a UI that allows users to enter food items and check their calories and nutritional information

202334419 인공지능학과 권형진
- [NLP] Implement food name and quantity extraction from natural language meal descriptions and link with DB to retrieve nutrition information

202334437 인공지능학과 김윤서
- create a Database for food nutrition information including calories/carbs/protein/fat/sodium

202333923 식품생명공학과 김현진 (조장)
- Evaluation logic based on KDRIs (19–29)  
- Calorie calculation & macronutrient analysis  
- Feedback and output generation  
- System integration management  
- Repository and project structure organization  
- Execution workflow & dependency setup  
- Coordination across UI, NLP, DB, and evaluation modules  
- End-to-end testing and validation  



