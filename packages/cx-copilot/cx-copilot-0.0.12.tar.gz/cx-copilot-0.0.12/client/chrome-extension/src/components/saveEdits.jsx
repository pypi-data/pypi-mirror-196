import React, { useEffect, useState } from "react";
import ApiClient from "../utils/client";
import "../styles/globals.css";

const SaveEdits = (props) => {
  const {
    clientId,
    ticketId,
    summary,
    citations,
    ticketSummaryRef,
    questionRefs,
    answerRefs,
  } = props;

  const API = new ApiClient();

  // Find diff in original tickets and edited tickets and update db
  const updateTickets = async () => {
    // TODO: bulk API to update multiple tickets

    const summarizedTicket = ticketSummaryRef.current.textContent;

    // Call API to update ticket
    if (summarizedTicket != summary) {
      console.log("summarizedTicket", summarizedTicket);
      // await API.patch("/tickets", {
      //   client_id: clientId,
      //   ticket_id: ticketId,
      //   summarized_question: summarizedTicket,
      // });
    }

    // TODO: add ticket_id/faq_id to citations
    for (let i = 0; i < citations.length; i++) {
      const citation = citations[i];
      const patchObj = {
        client_id: clientId,
        ticket_id: ticketId,
      }
      const summarizedQuestion = questionRefs[i].current.textContent;
      const summarizedAnswer = answerRefs[i].current.textContent;

      if (summarizedQuestion != citation.question) {
        patchObj.summarized_question = summarizedQuestion;
      }
      if (summarizedAnswer != citation.answer) {
        patchObj.summarized_answer = summarizedAnswer;
      }
      // Call API to update ticket
      if (summarizedQuestion != citation.question || summarizedAnswer != citation.answer) {
        console.log("patchObj", patchObj);
        // await API.patch("/tickets", patchObj);
      }
    }
    
  };

  return (
    <div className="flex space-x-2 justify-center items-center py-4">
      <button
        type="button"
        className="inline-flex items-center rounded border border-transparent bg-green-500 uppercase px-3 py-2 text-sm font-medium leading-4 text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        onClick={() => updateTickets()}>
        Save Edits
      </button>
    </div>
  );
};

export default SaveEdits;
