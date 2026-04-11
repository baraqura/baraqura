// src/core/ai/guardrail.js

const aiGuardrail = (riskScore, tenant) => {
    // ১. হাই-রিস্ক হলে সরাসরি ব্লক
    if (riskScore > 85) return "BLOCK";

    // ২. মিডিয়াম রিস্ক হলে এবং ফ্রি ইউজার হলে চ্যালেঞ্জ (CAPTCHA)
    if (riskScore > 50 && tenant.plan === 'free') return "CHALLENGE";

    // ৩. বাকি সব এলাউ
    return "ALLOW";
};

module.exports = { aiGuardrail };
