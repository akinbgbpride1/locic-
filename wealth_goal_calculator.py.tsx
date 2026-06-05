import React, { useState, useMemo } from 'react';

export default function WealthCalculator() {
  const [targetGoal, setTargetGoal] = useState(1000000);
  
  // State for dynamic accounts
  const [accounts, setAccounts] = useState([
    { id: 1, name: 'TFSA', type: 'tfsa', initialBalance: 20000, monthlyContribution: 500, annualReturn: 7.0 },
    { id: 2, name: 'RRSP', type: 'rrsp', initialBalance: 20000, monthlyContribution: 500, annualReturn: 6.5 },
    { id: 3, name: 'Non-Registered', type: 'non-reg', initialBalance: 10000, monthlyContribution: 200, annualReturn: 5.0 }
  ]);

  // useMemo ensures we only recalculate when inputs change
  const projection = useMemo(() => {
    let months = 0;
    const maxMonths = 600; // Cap at 50 years to prevent infinite loops if goal is unreachable
    
    // Initial state copy for calculation
    let currentAccountsState = accounts.map(acc => ({
      ...acc,
      currentBalance: acc.initialBalance,
      totalContributed: acc.initialBalance
    }));

    // Calculate total initial balance
    let totalCurrentBalance = currentAccountsState.reduce((sum, acc) => sum + acc.currentBalance, 0);

    // Handle edge case where target is already met
    if (totalCurrentBalance >= targetGoal) {
      return {
        years: 0,
        finalBalance: totalCurrentBalance,
        totalContributed: currentAccountsState.reduce((sum, acc) => sum + acc.totalContributed, 0),
        totalInterest: 0,
        accountBalances: currentAccountsState,
        isCapped: false,
      };
    }
    
    // Check if total contributions and returns are zero preventing growth
    const totalMonthlyContribution = currentAccountsState.reduce((sum, acc) => sum + acc.monthlyContribution, 0);
    const hasReturn = currentAccountsState.some(acc => acc.annualReturn > 0);
    
    if (totalMonthlyContribution === 0 && !hasReturn) {
         return {
          years: 50,
          finalBalance: totalCurrentBalance,
          totalContributed: totalCurrentBalance,
          totalInterest: 0,
          accountBalances: currentAccountsState,
          isCapped: true,
        };
    }

    // Run projection loop
    while (totalCurrentBalance < targetGoal && months < maxMonths) {
      totalCurrentBalance = 0; // Reset for this month's calculation
      
      currentAccountsState = currentAccountsState.map(acc => {
        const monthlyRate = (acc.annualReturn / 100) / 12;
        const newBalance = acc.currentBalance * (1 + monthlyRate) + acc.monthlyContribution;
        
        totalCurrentBalance += newBalance;
        
        return {
          ...acc,
          currentBalance: newBalance,
          totalContributed: acc.totalContributed + acc.monthlyContribution
        };
      });
      
      months += 1;
    }

    const years = (months / 12).toFixed(1);
    const totalContributed = currentAccountsState.reduce((sum, acc) => sum + acc.totalContributed, 0);
    const totalInterest = totalCurrentBalance - totalContributed;

    return {
      years: parseFloat(years),
      finalBalance: totalCurrentBalance,
      totalContributed,
      totalInterest,
      accountBalances: currentAccountsState, // Holds final state of each account
      isCapped: months >= maxMonths
    };
  }, [accounts, targetGoal]);

  const formatCurrency = (val) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(val);
  };

  const updateAccount = (id, field, value) => {
    setAccounts(accounts.map(acc => 
      acc.id === id ? { ...acc, [field]: value } : acc
    ));
  };

  const removeAccount = (id) => {
    if (accounts.length > 1) {
       setAccounts(accounts.filter(acc => acc.id !== id));
    } else {
       alert("You must have at least one account.");
    }
  };

  const addAccount = () => {
    const newId = accounts.length > 0 ? Math.max(...accounts.map(a => a.id)) + 1 : 1;
    setAccounts([...accounts, {
      id: newId,
      name: `New Account ${newId}`,
      type: 'custom',
      initialBalance: 0,
      monthlyContribution: 100,
      annualReturn: 5.0
    }]);
  };
  
  // Calculate current totals for display
  const currentTotalInitial = accounts.reduce((sum, acc) => sum + acc.initialBalance, 0);
  const currentTotalMonthly = accounts.reduce((sum, acc) => sum + acc.monthlyContribution, 0);

  const AccountCard = ({ account }) => (
    <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 mb-4 relative group">
      <button 
        onClick={() => removeAccount(account.id)}
        className="absolute top-2 right-2 text-slate-400 hover:text-red-500 bg-white rounded-full p-1 shadow-sm opacity-0 group-hover:opacity-100 transition-opacity"
        title="Remove Account"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
      </button>
      
      <div className="mb-3">
        <input 
          type="text" 
          value={account.name}
          onChange={(e) => updateAccount(account.id, 'name', e.target.value)}
          className="font-bold text-slate-800 bg-transparent border-b border-transparent hover:border-slate-300 focus:border-blue-500 focus:outline-none transition-colors w-full px-1"
          placeholder="Account Name"
        />
      </div>

      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-xs mb-1 text-slate-600">
            <span>Initial:</span>
            <span className="font-semibold">{formatCurrency(account.initialBalance)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={200000}
            step={1000}
            value={account.initialBalance}
            onChange={(e) => updateAccount(account.id, 'initialBalance', parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
        
        <div>
           <div className="flex justify-between text-xs mb-1 text-slate-600">
            <span>Monthly:</span>
            <span className="font-semibold">{formatCurrency(account.monthlyContribution)}</span>
          </div>
          <input
            type="range"
            min={0}
            max={5000}
            step={100}
            value={account.monthlyContribution}
            onChange={(e) => updateAccount(account.id, 'monthlyContribution', parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-500"
          />
        </div>

        <div>
           <div className="flex justify-between text-xs mb-1 text-slate-600">
            <span>Return:</span>
            <span className="font-semibold">{account.annualReturn.toFixed(1)}%</span>
          </div>
          <input
            type="range"
            min={0}
            max={15}
            step={0.1}
            value={account.annualReturn}
            onChange={(e) => updateAccount(account.id, 'annualReturn', parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-500"
          />
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        
        {/* Header Section */}
        <div className="mb-8 text-center md:text-left">
          <h1 className="text-3xl md:text-4xl font-extrabold text-slate-900 tracking-tight flex items-center justify-center md:justify-start gap-3">
            <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Multi-Account Wealth Calculator
          </h1>
          <p className="mt-2 text-slate-600 max-w-3xl">
            Build your custom financial strategy. Add accounts, set their specific balances, contributions, and expected returns to project your overall timeline to reaching your target goal.
          </p>
        </div>

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Account Inputs (Takes up 5 columns on large screens) */}
          <div className="lg:col-span-5 bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200 h-fit max-h-[800px] overflow-y-auto">
            <div className="flex justify-between items-center mb-6 sticky top-0 bg-white z-10 pb-2 border-b border-slate-100">
               <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                 <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                 Your Accounts
               </h2>
               <button 
                 onClick={addAccount}
                 className="text-sm bg-blue-50 text-blue-600 font-medium px-3 py-1.5 rounded-md hover:bg-blue-100 transition-colors flex items-center gap-1"
               >
                 <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"></path></svg>
                 Add Account
               </button>
            </div>

            {/* Render Account Cards */}
            <div className="space-y-4">
              {accounts.map(acc => (
                <AccountCard key={acc.id} account={acc} />
              ))}
            </div>
            
            {/* Summary of Inputs */}
            <div className="mt-6 pt-4 border-t border-slate-100 bg-slate-50 p-4 rounded-xl">
               <h3 className="text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">Total Current Inputs</h3>
               <div className="flex justify-between text-sm mb-1">
                 <span className="text-slate-500">Total Initial Portfolio:</span>
                 <span className="font-bold text-slate-800">{formatCurrency(currentTotalInitial)}</span>
               </div>
               <div className="flex justify-between text-sm">
                 <span className="text-slate-500">Total Monthly Contributions:</span>
                 <span className="font-bold text-slate-800">{formatCurrency(currentTotalMonthly)}</span>
               </div>
            </div>
            
            {/* Global Target Goal */}
            <div className="mt-6 pt-6 border-t border-slate-200">
               <div className="flex justify-between items-center mb-2">
                  <label className="text-base font-bold text-slate-800">Overall Target Goal</label>
                  <span className="text-lg font-bold text-slate-900 bg-slate-100 px-3 py-1 rounded-md">
                    {formatCurrency(targetGoal)}
                  </span>
                </div>
                <input
                  type="range"
                  min={100000}
                  max={5000000}
                  step={50000}
                  value={targetGoal}
                  onChange={(e) => setTargetGoal(parseFloat(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>

          </div>

          {/* Right Column: Outputs (Takes up 7 columns on large screens) */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Top Dashboard Card */}
            <div className="bg-slate-900 p-8 rounded-2xl shadow-xl text-white relative overflow-hidden">
              {/* Decorative background circle */}
              <div className="absolute -right-16 -top-16 w-64 h-64 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30"></div>
              
              <div className="relative z-10">
                <h2 className="text-blue-300 text-sm uppercase tracking-wider font-semibold mb-2">Time to Reach Combined Goal</h2>
                <div className="flex items-baseline gap-2 mb-8">
                  {projection.isCapped ? (
                    <span className="text-5xl md:text-7xl font-black text-red-400">50+</span>
                  ) : (
                    <span className="text-5xl md:text-7xl font-black">{projection.years}</span>
                  )}
                  <span className="text-xl md:text-2xl text-slate-300 font-medium">Years</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 border-t border-slate-700 pt-6">
                  <div>
                    <p className="text-slate-400 text-sm mb-1">Total Principal Contributed</p>
                    <p className="text-2xl font-bold">{formatCurrency(projection.totalContributed)}</p>
                  </div>
                  <div>
                    <p className="text-slate-400 text-sm mb-1">Total Compound Interest</p>
                    <p className="text-2xl font-bold text-emerald-400">{formatCurrency(projection.totalInterest)}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Dynamic Account Allocation Breakdown Card */}
            <div className="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200">
              <div className="flex justify-between items-end mb-6">
                <div>
                  <h3 className="text-lg font-bold text-slate-800">Projected Final Allocation</h3>
                  <p className="text-sm text-slate-500 mt-1">Based on individual account growth</p>
                </div>
                <div className="text-right hidden sm:block">
                  <p className="text-xs text-slate-400">Total Final Balance</p>
                  <p className="font-bold text-slate-800">{formatCurrency(projection.finalBalance)}</p>
                </div>
              </div>

              {/* Dynamic Progress Bar Visualization */}
              <div className="w-full h-4 flex rounded-full overflow-hidden mb-6 bg-slate-100">
                {projection.accountBalances.map((acc, index) => {
                  const percentage = ((acc.currentBalance / projection.finalBalance) * 100).toFixed(1);
                  // Assign colors based on index to keep it distinct
                  const colors = ['bg-blue-500', 'bg-emerald-500', 'bg-indigo-400', 'bg-amber-400', 'bg-rose-400', 'bg-cyan-500'];
                  const colorClass = colors[index % colors.length];
                  
                  return (
                    <div 
                      key={acc.id} 
                      className={`h-full ${colorClass}`} 
                      style={{ width: `${percentage}%` }}
                      title={`${acc.name}: ${percentage}%`}
                    ></div>
                  );
                })}
              </div>

              {/* Dynamic Breakdown Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
                 {projection.accountBalances.map((acc, index) => {
                   const percentage = ((acc.currentBalance / projection.finalBalance) * 100).toFixed(1);
                   const colors = [
                     { bg: 'bg-blue-50', text: 'text-blue-900', border: 'border-blue-100', dot: 'bg-blue-500', badge: 'text-blue-600 bg-blue-100' },
                     { bg: 'bg-emerald-50', text: 'text-emerald-900', border: 'border-emerald-100', dot: 'bg-emerald-500', badge: 'text-emerald-600 bg-emerald-100' },
                     { bg: 'bg-indigo-50', text: 'text-indigo-900', border: 'border-indigo-100', dot: 'bg-indigo-400', badge: 'text-indigo-600 bg-indigo-100' },
                     { bg: 'bg-amber-50', text: 'text-amber-900', border: 'border-amber-100', dot: 'bg-amber-400', badge: 'text-amber-600 bg-amber-100' },
                     { bg: 'bg-rose-50', text: 'text-rose-900', border: 'border-rose-100', dot: 'bg-rose-400', badge: 'text-rose-600 bg-rose-100' },
                     { bg: 'bg-cyan-50', text: 'text-cyan-900', border: 'border-cyan-100', dot: 'bg-cyan-500', badge: 'text-cyan-600 bg-cyan-100' }
                   ];
                   const theme = colors[index % colors.length];

                   return (
                    <div key={acc.id} className={`${theme.bg} rounded-xl p-4 border ${theme.border}`}>
                      <div className="flex items-center gap-2 mb-2">
                        <div className={`w-3 h-3 rounded-full ${theme.dot}`}></div>
                        <span className={`font-semibold ${theme.text} truncate max-w-[100px]`} title={acc.name}>{acc.name}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ml-auto ${theme.badge}`}>{percentage}%</span>
                      </div>
                      <p className={`text-lg font-bold ${theme.text}`}>{formatCurrency(acc.currentBalance)}</p>
                      <div className="mt-2 text-xs text-slate-500 space-y-1">
                        <div className="flex justify-between"><span>Principal:</span> <span>{formatCurrency(acc.totalContributed)}</span></div>
                        <div className="flex justify-between"><span>Interest:</span> <span>{formatCurrency(acc.currentBalance - acc.totalContributed)}</span></div>
                      </div>
                    </div>
                   );
                 })}
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
}