document.addEventListener('DOMContentLoaded', () => {
    const predictBtn = document.getElementById('predictBtn');
    const newsInput = document.getElementById('newsInput');
    const resultSection = document.getElementById('resultSection');
    const resultCard = document.getElementById('resultCard');
    const resultTitle = document.getElementById('resultTitle');
    const resultIcon = document.querySelector('.result-icon');
    const errorMsg = document.getElementById('errorMsg');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const charCount = document.getElementById('charCount');
    const demoBtn = document.getElementById('demoBtn');

    const sampleText = "BREAKING: Scientists have discovered a new species of glowing mushrooms in the Amazon rainforest that can purify contaminated water in a matter of hours. The groundbreaking find was published in Nature today. According to Dr. Elena Rostova, the lead researcher on the expedition, the mushrooms absorb heavy metals and neutralize harmful bacteria.";

    if (demoBtn) {
        demoBtn.addEventListener('click', () => {
            newsInput.value = '';
            let i = 0;
            predictBtn.disabled = true;
            demoBtn.style.opacity = '0.5';
            demoBtn.style.pointerEvents = 'none';
            
            errorMsg.classList.add('hidden');
            resultSection.classList.add('hidden');
            
            const typingEffect = setInterval(() => {
                newsInput.value += sampleText.charAt(i);
                charCount.textContent = newsInput.value.length;
                newsInput.style.boxShadow = '0 0 15px rgba(88, 166, 255, 0.15), inset 0 2px 4px rgba(0,0,0,0.1)';
                i++;
                if (i >= sampleText.length) {
                    clearInterval(typingEffect);
                    predictBtn.disabled = false;
                    demoBtn.style.opacity = '1';
                    demoBtn.style.pointerEvents = 'auto';
                }
            }, 10);
        });
    }

    const liveNewsBtn = document.getElementById('liveNewsBtn');
    const liveNewsContainer = document.getElementById('liveNewsContainer');
    const liveNewsList = document.getElementById('liveNewsList');

    if (liveNewsBtn) {
        liveNewsBtn.addEventListener('click', async () => {
            const originalText = liveNewsBtn.innerHTML;
            liveNewsBtn.innerHTML = '<span class="demo-icon">⏳</span> Fetching...';
            liveNewsBtn.disabled = true;
            errorMsg.classList.add('hidden');
            
            try {
                const response = await fetch('/fetch_live_news');
                const data = await response.json();
                
                if (!response.ok) throw new Error(data.error || 'Failed to fetch news');
                
                liveNewsList.innerHTML = '';
                data.news.forEach(article => {
                    const btn = document.createElement('button');
                    btn.className = 'demo-btn';
                    btn.style.width = '100%';
                    btn.style.textAlign = 'left';
                    btn.style.padding = '12px';
                    btn.style.whiteSpace = 'normal';
                    btn.style.height = 'auto';
                    btn.style.justifyContent = 'flex-start';
                    btn.style.display = 'block';
                    btn.style.marginBottom = '8px';
                    
                    const descText = article.text.length > article.title.length 
                        ? article.text.substring(article.title.length + 2, 120) + '...'
                        : '';
                    
                    btn.innerHTML = `<strong style="display:block; margin-bottom:4px; font-size:15px; color:#fff;">${article.title}</strong><span style="font-size:13px; color:#aaa; line-height:1.4;">${descText}</span>`;
                    
                    btn.addEventListener('click', () => {
                        newsInput.value = article.text;
                        charCount.textContent = newsInput.value.length;
                        newsInput.style.boxShadow = '0 0 15px rgba(88, 166, 255, 0.15), inset 0 2px 4px rgba(0,0,0,0.1)';
                        liveNewsContainer.classList.add('hidden');
                        resultSection.classList.add('hidden');
                        errorMsg.classList.add('hidden');
                    });
                    
                    liveNewsList.appendChild(btn);
                });
                
                liveNewsContainer.classList.remove('hidden');
            } catch (error) {
                console.error(error);
                showError('Could not fetch live news: ' + error.message);
            } finally {
                liveNewsBtn.innerHTML = originalText;
                liveNewsBtn.disabled = false;
            }
        });
    }

    // Add glowing effect to textarea on input
    newsInput.addEventListener('input', function() {
        charCount.textContent = this.value.length;
        if (this.value.trim().length > 0) {
            this.style.boxShadow = '0 0 15px rgba(88, 166, 255, 0.15), inset 0 2px 4px rgba(0,0,0,0.1)';
        } else {
            this.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.1)';
        }
        errorMsg.classList.add('hidden');
    });

    predictBtn.addEventListener('click', async () => {
        const textToAnalyze = newsInput.value.trim();
        
        if (!textToAnalyze) {
            showError('Please enter some text to analyze.');
            newsInput.focus();
            return;
        }

        // Setup Loading State
        predictBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        loader.classList.remove('hidden');
        resultSection.classList.add('hidden');
        errorMsg.classList.add('hidden');
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: textToAnalyze })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Server responded with an error');
            }
            
            showResult(data.prediction, data.is_real, data.verified_headline);
            
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'Failed to connect to the server. Please try again.');
        } finally {
            // Restore Original State
            predictBtn.disabled = false;
            btnText.textContent = 'Analyze Authenticity';
            loader.classList.add('hidden');
        }
    });
    
    function showResult(prediction, isReal, verifiedHeadline) {
        // Reset classes
        resultCard.className = 'result-card';
        
        // Setup new format
        if (isReal) {
            resultCard.classList.add('is-real');
            resultIcon.textContent = '🛡️';
            resultTitle.textContent = 'Authentic News';
        } else {
            resultCard.classList.add('is-fake');
            resultIcon.textContent = '⚠️';
            resultTitle.textContent = 'Likely Fake News';
        }

        // Handle verified headline text
        let desc = document.getElementById('resultDesc');
        if (verifiedHeadline) {
            desc.innerHTML = `Our AI detected this as a <strong>Live News Event</strong>.<br><span style="font-size: 0.85rem; color: #1ed760;">Verified matches headline: "${verifiedHeadline}"</span>`;
        } else {
            desc.textContent = "Our AI has analyzed the patterns in the text to determine its authenticity.";
        }
        
        resultSection.classList.remove('hidden');
        
        // Scroll to result slightly
        setTimeout(() => {
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }
    
    function showError(message) {
        errorMsg.textContent = message;
        errorMsg.classList.remove('hidden');
        errorMsg.style.animation = 'shake 0.5s ease-in-out';
        
        // Remove animation after it plays
        setTimeout(() => {
            errorMsg.style.animation = '';
        }, 500);
    }
});

// Add shake animation dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        50% { transform: translateX(5px); }
        75% { transform: translateX(-5px); }
    }
`;
document.head.appendChild(style);
