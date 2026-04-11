const suggestAction = (threatData) => {
  return {
    id: Date.now(),
    action: "INCREASE_RATE_LIMIT",
    reason: "Sudden spike in traffic from IP 192.168.1.1",
    confidence: 0.89,
    status: "PENDING_APPROVAL" // Human must click 'Approve'
  };
};
