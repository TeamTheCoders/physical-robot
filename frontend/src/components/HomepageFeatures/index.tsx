import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';

type FeatureItem = {
  title: string;
  description: ReactNode;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description: (
      <>
        Get hands-on with the Robot Operating System (ROS 2), the essential framework for robotics. This module covers the core concepts you need to build, simulate, and manage robotic systems using Gazebo.
      </>
    ),
    link: '/docs/module1-ros/architecture-communication',
  },
  {
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description: (
      <>
        Learn to build and work with digital twins of your robots. This module explores advanced simulation techniques in Gazebo and Unity, focusing on humanoid robot design, two-legged walking, and how humans and robots can interact effectively.
      </>
    ),
    link: '/docs/module2-simulation/gazebo-setup-basics',
  },
  {
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
    description: (
      <>
        Dive into the world of artificial intelligence for robotics with NVIDIA Isaac. In this module, you'll learn how to give your robot a 'brain', enabling it to understand and respond to voice commands and make intelligent decisions.
      </>
    ),
    link: '/docs/module3-ai/omniverse-usd-isaac-sim',
  },
    {
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: (
      <>
       This final module brings everything together. You'll explore how Large Language Models (LLMs) can act as the 'mind' of a robot, enabling it to understand speech, see the world, and take action. We'll also cover how to build a complete, autonomous humanoid robot and discuss the ethical implications of this technology.
      </>
    ),
    link: '/docs/module4-vla/humanoid-kinematics-dynamics',
  }
];

function Feature({ title, description, link }: FeatureItem) {
  return (
    <div className="w-full p-4 md:w-1/2 lg:w-1/4">
      <Link to={link} className="block h-full no-underline hover:no-underline group">
        <div className="h-full p-6 transition-all duration-300 bg-white border shadow-sm border-slate-200 rounded-2xl hover:shadow-xl hover:shadow-purple-500/20 hover:-translate-y-2 dark:bg-white/5 dark:border-white/10 dark:backdrop-blur-sm dark:hover:bg-white/10">
          <h3 className="mb-3 text-xl font-bold transition-colors text-slate-900 group-hover:text-blue-600 dark:text-white dark:group-hover:text-blue-400">
            {title}
          </h3>
          <p className="text-sm leading-relaxed text-slate-600 group-hover:text-slate-700 dark:text-slate-400 dark:group-hover:text-slate-300">
            {description}
          </p>
        </div>
      </Link>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className="w-full">
      <div className="flex flex-wrap -m-4">
        {FeatureList.map((props, idx) => (
          <Feature key={idx} {...props} />
        ))}
      </div>
    </section>
  );
}