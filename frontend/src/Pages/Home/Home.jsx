import React, { useState } from "react";
import styles from "./Home.module.scss";
import PredictionComponent from "./Prediction/Prediction";

const Home = () => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);

  const handleTextChange = (e) => {
    setText(e.target.value);
  };
  const handleUpload = async () => {
    setLoading(true);
    try {
      // Ensure the text variable is properly defined and formatted
      if (!text) {
        throw new Error("Text is not defined");
      }

      const response = await fetch("https://aivshuman.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }), // Ensure text is correctly JSON.stringified
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error("Error during fetch:", error);
    } finally {
      setLoading(false);
    }
  };

  // Word counter function
  const wordCount = text.trim().split(/\s+/).filter(Boolean).length;

  return (
    <div className={styles.homeContainer}>
      {/* <div className={styles.home1}> */}
      <div className={styles.titleContainer}>
        <h1>Detect the AI content in your text</h1>
      </div>
      <div className={styles.textAreaContainer}>
        <textarea
          className={styles.formControl}
          rows="25"
          value={text}
          onChange={handleTextChange}
          placeholder="Write your text here..."
        />
        <div className={styles.wordCounter}>Word Count: {wordCount}</div>
        <button className={styles.uploadButton} onClick={handleUpload}>
          Upload
        </button>
      </div>
      {loading && <div className={styles.loading}>Loading...</div>}
      {prediction !== null && <PredictionComponent prediction={prediction} />}
      {/* </div> */}

      {/* <div className={styles.whyUseWebsite}> */}
      {/* <h2>Why to use US?</h2>
      <div className={styles.cardContainer}>
        <div className={styles.card}>
          <h3>Accurate Analysis</h3>
          <p>
            Our AI technology provides accurate analysis of your text, ensuring reliable
            results.
          </p>
        </div>
        <div className={styles.card}>
          <h3>Time-saving</h3>
          <p>
            Save time by automating the process of analyzing text content for AI elements.
          </p>
        </div>
        <div className={styles.card}>
          <h3>User-friendly Interface</h3>
          <p>
            Our website offers an intuitive and easy-to-use interface for seamless text
            analysis.
          </p>
        </div>
      </div> */}
    </div>
    // </div>
  );
};

export default Home;
