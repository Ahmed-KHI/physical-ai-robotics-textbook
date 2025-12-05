import React, { JSX } from 'react';
import Link from '@docusaurus/Link';
import Logo from '@site/static/img/logo.svg';

import styles from './styles.module.css';

type FooterLink = {
  label: string;
  to?: string;
  href?: string;
};

type FooterColumnData = {
  title: string;
  links: FooterLink[];
};

const columns: FooterColumnData[] = [
  {
    title: 'Curriculum',
    links: [
      {label: 'Course Overview', to: '/docs/intro'},
      {label: 'Module 1: ROS 2 Basics', to: '/docs/module-1/intro'},
      {label: 'Module 2: Simulation', to: '/docs/module-2/intro'},
      {label: 'Module 3: Isaac Lab', to: '/docs/module-3/intro'},
    ],
  },
  {
    title: 'Resources',
    links: [
      {label: 'Documentation', to: '/docs/intro'},
      {label: 'Getting Started', to: '/docs/intro'},
    ],
  },
];

const socialLinks = [
  {label: 'GitHub', href: 'https://github.com/Ahmed-KHI/physical-ai-robotics-textbook'},
  {label: 'Demo Video', href: '#'},
];

const stats = [
  {value: 'RAG', label: 'AI Chatbot'},
  {value: '95%', label: 'Cost Savings'},
  {value: '4', label: 'AI Features'},
];

function FooterColumn({title, links}: FooterColumnData) {
  return (
    <div className={styles.column}>
      <p className={styles.columnTitle}>{title}</p>
      <ul>
        {links.map((link) => (
          <li key={link.label}>
            {link.to ? (
              <Link to={link.to} className={styles.link}>
                {link.label}
              </Link>
            ) : (
              <a href={link.href} className={styles.link} target="_blank" rel="noreferrer">
                {link.label}
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function Footer(): JSX.Element {
  const year = new Date().getFullYear();

  return (
    <footer className={styles.footer}>
      <div className={styles.ctaCard}>
        <div>
          <p className={styles.eyebrow}>GIAIC Hackathon 2025</p>
          <h2>
            Physical AI & <span>Humanoid Robotics</span>
          </h2>
          <p>
            AI-native textbook with RAG chatbot, Qdrant vector search, GPT-3.5-turbo optimization (95% cost savings),
            text selection queries, and adaptive learning features.
          </p>
        </div>
        <div className={styles.ctaActions}>
          <Link className={styles.primaryCta} to="/docs/intro">
            Start Learning
          </Link>
        </div>
      </div>

      <div className={styles.statsRow}>
        {stats.map((stat) => (
          <div key={stat.label} className={styles.statCard}>
            <span>{stat.value}</span>
            <p>{stat.label}</p>
          </div>
        ))}
      </div>

      <div className={styles.main}>
        <div className={styles.brand}>
          <div className={styles.brandLogo}>
            <Logo className={styles.logoIcon} role="img" aria-label="Physical AI Logo" />
            <div>
              <p>Physical AI & Robotics</p>
              <span>GIAIC Hackathon 2025 • AI-Native Textbook</span>
            </div>
          </div>
          <p className={styles.brandCopy}>
            Built for GIAIC Hackathon 2025. Features RAG chatbot with Qdrant vector search, FastAPI backend,
            React frontend, GPT-3.5-turbo optimization, and production-ready authentication—teaching Physical AI & Humanoid Robotics.
          </p>
          <div className={styles.socials}>
            {socialLinks.map((social) => (
              <a key={social.label} href={social.href} target="_blank" rel="noreferrer" className={styles.socialLink}>
                {social.label}
              </a>
            ))}
          </div>
        </div>
        <div className={styles.columns}>
          {columns.map((column) => (
            <FooterColumn key={column.title} {...column} />
          ))}
        </div>
      </div>

      <div className={styles.bottomBar}>
        <p>© {year} Physical AI & Robotics • GIAIC Hackathon 2025</p>
        <div className={styles.bottomLinks}>
          <Link to="/docs/intro">Documentation</Link>
          <a href="https://github.com/Ahmed-KHI/physical-ai-robotics-textbook" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>
    </footer>
  );
}
