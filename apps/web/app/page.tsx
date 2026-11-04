
const features = [
  {
    number: "01",
    icon: "⚖",
    title: "Know Your Rights",
    description:
      "Understand women's legal rights, important laws and available government support through simple explanations.",
    link: "#rights",
  },
  {
    number: "02",
    icon: "✳",
    title: "AI Legal Assistant",
    description:
      "Ask questions in your preferred language and receive context-aware guidance grounded in legal resources.",
    link: "#assistant",
  },
  {
    number: "03",
    icon: "▤",
    title: "FIR Assistance",
    description:
      "Understand the complaint process, prepare incident details and learn what documents may be required.",
    link: "#support",
  },
];

const steps = [
  ["01", "Share your concern", "Ask a question or explore a legal topic."],
  ["02", "Get clear guidance", "Understand relevant rights and legal procedures."],
  ["03", "Explore your next step", "Find useful resources and support options."],
];

export default function Home() {
  return (
    <main>
      <nav className="navbar">
        <a href="#" className="brand">
          <span className="brand-mark">K</span>
          <span>Kural<span className="brand-light">AI</span></span>
        </a>

        <div className="nav-links">
          <a href="#about">About</a>
          <a href="#features">What We Offer</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#support">Support</a>
        </div>

        <a href="#assistant" className="nav-cta">
          Explore KuralAI <span>↗</span>
        </a>
      </nav>

      <section className="hero" id="about">
        <div className="hero-content">
          <div className="eyebrow">
            <span className="status-dot" />
            LEGAL AWARENESS. ACCESSIBLE TO EVERY WOMAN.
          </div>

          <h1>
            Your rights.
            <br />
            Your voice.
            <br />
            <span>Your Kural.</span>
          </h1>

          <p className="hero-description">
            Understanding your rights should never be complicated.
            KuralAI brings legal awareness, guidance and support closer
            to every woman — in a language she understands.
          </p>

          <div className="hero-actions">
            <a href="#assistant" className="primary-btn">
              Explore Legal Assistance <span>→</span>
            </a>
            <a href="#features" className="secondary-btn">
              Discover KuralAI
            </a>
          </div>

          <div className="hero-note">
            <span>✳</span>
            Knowledge is the first step towards empowerment.
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-orbit orbit-one" />
          <div className="visual-orbit orbit-two" />

          <div className="visual-center">
            <span className="visual-symbol">K</span>
            <span className="visual-name">KuralAI</span>
            <span className="visual-caption">HER VOICE MATTERS</span>
          </div>

          <div className="floating-card card-top">
            <span className="floating-icon">⚖</span>
            <div>
              <strong>Know your rights</strong>
              <small>Knowledge creates confidence</small>
            </div>
          </div>

          <div className="floating-card card-bottom">
            <span className="floating-icon">✳</span>
            <div>
              <strong>Guidance without barriers</strong>
              <small>Accessible. Multilingual. Supportive.</small>
            </div>
          </div>
        </div>

        <div className="hero-index">
          <span>01</span>
          <span className="index-line" />
          <span>EMPOWERMENT THROUGH AWARENESS</span>
        </div>
      </section>

      <section className="intro-section">
        <div>
          <span className="section-label">WHY KURALAI EXISTS</span>
          <h2>
            Justice begins with
            <br />
            <span>knowing your rights.</span>
          </h2>
        </div>
        <p>
          Legal information can feel overwhelming, especially when someone
          doesn't know where to begin. KuralAI aims to make that first step
          simpler by bringing essential legal knowledge and support into
          one accessible platform.
        </p>
      </section>

      <section className="features-section" id="features">
        <div className="section-heading">
          <div>
            <span className="section-label">WHAT WE OFFER</span>
            <h2>Support that starts with <span>understanding.</span></h2>
          </div>
          <p>One platform. Multiple pathways to awareness and support.</p>
        </div>

        <div className="feature-grid">
          {features.map((feature) => (
            <article className="feature-card" key={feature.number}>
              <div className="feature-top">
                <span className="feature-number">{feature.number}</span>
                <span className="feature-icon">{feature.icon}</span>
              </div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
              <a href={feature.link} className="feature-link">
                Explore feature <span>↗</span>
              </a>
            </article>
          ))}
        </div>
      </section>

      <section className="assistant-banner" id="assistant">
        <div>
          <span className="section-label">A SPACE TO ASK. A SPACE TO LEARN.</span>
          <h2>
            Sometimes, all you need
            <br />
            is <span>someone to guide you.</span>
          </h2>
          <p>
            Explore the KuralAI legal assistant experience and discover
            how technology can make legal awareness more accessible.
          </p>
          <a href="#support" className="light-btn">
            Explore the experience <span>→</span>
          </a>
        </div>
        <div className="assistant-decoration">
          <div className="chat-bubble">
            <span>✳</span>
            <p>Every question deserves to be heard.</p>
          </div>
          <div className="chat-bubble chat-bubble-small">
            Your voice matters.
          </div>
        </div>
      </section>

      <section className="steps-section" id="how-it-works">
        <span className="section-label">HOW IT WORKS</span>
        <h2>Three steps towards <span>awareness.</span></h2>

        <div className="steps-grid">
          {steps.map(([number, title, description]) => (
            <article className="step-card" key={number}>
              <span className="step-number">{number}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="support-section" id="support">
        <div>
          <span className="section-label">YOU ARE NOT ALONE</span>
          <h2>Help should never be <span>out of reach.</span></h2>
          <p>
            If you are in immediate danger in India, contact emergency
            services at 112. KuralAI is an information and guidance
            platform, not an emergency response service.
          </p>
        </div>
        <a href="https://112.gov.in/" target="_blank" rel="noreferrer"
          className="emergency-btn">
          Emergency Help – 112 ↗
        </a>
      </section>

      <footer className="footer">
        <a href="#" className="brand footer-brand">
          <span className="brand-mark">K</span>
          <span>Kural<span className="brand-light">AI</span></span>
        </a>
        <p>Her Voice. Her Rights. Her Kural.</p>
        <span>© 2026 KuralAI. Built for empowerment.</span>
      </footer>
    </main>
  );
}
