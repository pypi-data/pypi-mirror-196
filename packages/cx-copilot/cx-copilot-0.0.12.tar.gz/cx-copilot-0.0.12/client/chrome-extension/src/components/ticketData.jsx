import React, { useEffect, useState, useRef } from 'react';
import Summary from './summary';
import Citations from './citations';
import Feedback from './feedback';
import NextCompletion from './nextCompletion';
import ApiClient from "../utils/client";
import '../styles/globals.css'

const TicketData = (props) => {
  const {
    clientId,
    ticketId,
    completionIdx,
    completionsLength,
    completion,
    setNextCompletionIdx,
    setClientId,
  } = props;

  const ticketSummaryRef = useRef(null);
  const questionRefs = [];
  for (let i = 0; i < completion.citations.length; i++) {
    questionRefs.push(useRef(null));
  }
  const answerRefs = [];
  for (let i = 0; i < completion.citations.length; i++) {
    answerRefs.push(useRef(null));
  }

  const API = new ApiClient();

  // Update ticket summarized question/answer
  const updateTicket = async (ticketId, summarized_question, summarized_answer) => {
    const patchObj = {
      client_id: clientId,
      ticket_id: ticketId,
    }

    if (summarized_question) {
      patchObj.summarized_question = summarized_question;
    }
    if (summarized_answer) {
      patchObj.summarized_answer = summarized_answer;
    }

    console.log("patchObj", patchObj)

    // await API.patch("/tickets", patchObj);
  };

  const bulkUpdateTickets = async () => {
  }

  return (
    <>
      <Summary
        ticketId={ticketId}
        summary={completion.summary}
        ticketSummaryRef={ticketSummaryRef}
        updateTicket={updateTicket}/>

      <Citations
        citations={completion.citations || []}
        questionRefs={questionRefs}
        answerRefs={answerRefs}
        updateTicket={updateTicket}/>

      <Feedback
        clientId={clientId}
        ticketId={ticketId}
        completionIdx={completionIdx}
        completionsLength={completionsLength}
        completion={completion}
        version={1} // hardcoded version number
        setNextCompletionIdx={setNextCompletionIdx}/>

      <NextCompletion
        completionIdx={completionIdx}
        completionsLength={completionsLength}
        setNextCompletionIdx={setNextCompletionIdx}
        />
    </>
  )

}

export default TicketData