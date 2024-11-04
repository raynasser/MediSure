require('dotenv').config();

const express = require('express');
const cors = require('cors');
const { OpenAI } = require("openai");
const fs = require('fs');
const csv = require('csv-parser');

const app = express();
app.use(cors());
app.use(express.json());

// OpenAI API Configuration
// const openai = new OpenAI({
//   apiKey: ''
// });'


const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: process.env.API_KEY,
});


// Load CSV data
let dataset = [];
fs.createReadStream('../data/raw_data/fin/final_final_fdi_ddi.csv')
  .pipe(csv())
  .on('data', (row) => {
    dataset.push(row);
  });

// Function to recognize drugs using OpenAI
async function drugRecognizer(text) {
  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
      { role: 'system', content: 'Identify drugs in the text and return them as a JSON object.' },
      { role: 'user', content: text }
    ]
  });

  const recognizedDrugs = JSON.parse(response.choices[0].message.content).drugs;
  return [...new Set(recognizedDrugs)]; // Remove duplicates
}

// Function to retrieve side effects using OpenAI
async function drugSideEffect(drug) {
  const response = await openai.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [
      { role: 'system', content: `Identify the side effects of the drug "${drug}". Return the side effects as a list in plain text format.` },
      { role: 'user', content: `What are the side effects of ${drug}?` }
    ]
  });

  const sideEffectsText = response.choices[0].message.content;

  // Extract list of side effects from the text
  const sideEffects = sideEffectsText.split(/\n|•|-|\d\./).map(effect => effect.trim()).filter(effect => effect.length > 0);

  return sideEffects;
}

// Endpoint to process chatbot input
app.post('/api/process-chatbot', async (req, res) => {
  const { text } = req.body;

  try {
    const drugs = await drugRecognizer(text);

    const recommendations = await Promise.all(drugs.map(async (drug) => {
      // Filter for food-drug interactions based on the recognized drugs
      const recommendedFoods = dataset
        .filter(entry => entry.drug.toLowerCase() === drug.toLowerCase() && entry.fdi_tau_score >= 0 && entry.food.trim().toLowerCase() !== 'food') // Exclude "food"
        .map(entry => entry.food);

      const foodsToAvoid = dataset
        .filter(entry => entry.drug.toLowerCase() === drug.toLowerCase() && entry.fdi_tau_score < 0 && entry.food.trim().toLowerCase() !== 'food') // Exclude "food"
        .map(entry => entry.food);

      // Find drugs to avoid based on drug-drug interaction (ddi_tau_score < 0)
      const drugsToAvoid = dataset
        .filter(entry => entry.Drug_A === drug && entry.ddi_tau_score < 0.0)  // Simplified check
        .map(entry => entry.Drug_B);  // Return Drug_B as the interacting drug

      const sideEffects = await drugSideEffect(drug);

      return {
        drug,
        recommended: [...new Set(recommendedFoods)], // Remove duplicates
        to_avoid: [...new Set(foodsToAvoid)], // Remove duplicates
        dTo_avoid: [...new Set(drugsToAvoid)], // Remove duplicates from drug-drug interaction
        side_effects: sideEffects,
      };
    }));

    res.json(recommendations);
  } catch (error) {
    res.status(500).json({ message: 'Error processing input' });
  }
});


// Start the Node.js server
app.listen(5001, () => {
  console.log('Server is running on port 5001');
  console.log("API Key:", process.env.API_KEY);
});
