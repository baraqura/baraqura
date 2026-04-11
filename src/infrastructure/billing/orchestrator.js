// src/infrastructure/billing/orchestrator.js

const trackUsage = async (tenant) => {
    // এখানে আমরা চেক করছি ইউজারের লিমিট শেষ কি না
    if (tenant.currentUsage >= tenant.limits) {
        throw new Error("QUOTA_EXCEEDED");
    }

    // বাস্তবে এখানে DB আপডেট হবে: tenant.currentUsage += 1
    console.log(`💰 Billing: Tracking usage for ${tenant.id}. Current: ${tenant.currentUsage + 1}`);
    
    return true;
};

module.exports = { trackUsage };
