import React, { useState } from "react";
import axios from "axios";
import "./App.css";
function App() {
    const [applicantName, setApplicantName] = useState("");
    const [annualIncome, setAnnualIncome] = useState("");
    const [documentImage, setDocumentImage] = useState(null);
    const [w2Image, setW2Image] = useState(null);
    const [responseMessage, setResponseMessage] = useState("");

    const [comparisonResults, setComparisonResults] = useState({
        nameMatchInDocument: false,
        nameMatchInW2: false,
        incomeMatchInW2: false,
    });
    const [loanDetails, setLoanDetails] = useState({
        approxLoanAmount: null,
        interestRate: null,
        loanTermYears: null,
        monthlyPayment: null
    });
    const [showComparisonResults, setShowComparisonResults] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("applicant_name", applicantName);
        formData.append("monthly_income", annualIncome);
        formData.append("document_image", documentImage);
        if (w2Image) formData.append("w2_image", w2Image);

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/loan-application/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });

            setResponseMessage("Loan application submitted successfully!");

            setComparisonResults({
                nameMatchInDocument: response.data.name_match_in_document,
                nameMatchInW2: response.data.name_match_in_w2,
                incomeMatchInW2: response.data.income_match_in_w2
            });
            setLoanDetails({
                approxLoanAmount: response.data.approx_loan_amount,
                interestRate: response.data.interest_rate,
                loanTermYears: response.data.loan_term_years,
                monthlyPayment: response.data.monthly_payment
            });
            setShowComparisonResults(true);
        } catch (error) {
            console.error("Error submitting loan application:", error);
            setResponseMessage("Failed to submit the loan application.");
            setShowComparisonResults(false);
        }
    };

    return (
        <div className="App">
            <h1>Loan Application Form</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Applicant Name:</label>
                    <input
                        type="text"
                        value={applicantName}
                        onChange={(e) => setApplicantName(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Annual Income:</label>
                    <input
                        type="number"
                        value={annualIncome}
                        onChange={(e) => setAnnualIncome(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Identification Card:</label>
                    <input
                        type="file"
                        onChange={(e) => setDocumentImage(e.target.files[0])}
                        accept="image/*"
                        required
                    />
                </div>
                <div>
                    <label>W2 Form Image:</label>
                    <input
                        type="file"
                        onChange={(e) => setW2Image(e.target.files[0])}
                        accept="image/*"
                    />
                </div>
                <button type="submit">Submit Application</button>
            </form>
            {responseMessage && <p className="response-message">{responseMessage}</p>}

            {showComparisonResults && (
                <div className="comparison-results">
                    <h3>Comparison Results:</h3>
                    <p>
                        Name in Document:{" "}
                        {comparisonResults.nameMatchInDocument ? (
                            <span className="green-check">✔️</span>
                        ) : (
                            <span className="red-cross">✘</span>
                        )}
                    </p>
                    <p>
                        Name in W2:{" "}
                        {comparisonResults.nameMatchInW2 ? (
                            <span className="green-check">✔️</span>
                        ) : (
                            <span className="red-cross">✘</span>
                        )}
                    </p>
                    <p>
                        Income in W2:{" "}
                        {comparisonResults.incomeMatchInW2 ? (
                            <span className="green-check">✔️</span>
                        ) : (
                            <span className="red-cross">✘</span>
                        )}
                    </p>
                    <h3>Loan Details:</h3>
                    <p>Approximate Loan Amount: ${loanDetails.approxLoanAmount?.toLocaleString()}</p>
                    <p>Interest Rate: {loanDetails.interestRate}%</p>
                    <p>Loan Term: {loanDetails.loanTermYears} years</p>
                    <p>Monthly Payment: ${loanDetails.monthlyPayment?.toLocaleString()}</p>
                </div>
            )}
        </div>
    );
}

export default App;
