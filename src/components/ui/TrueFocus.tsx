import { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';

const TrueFocus = ({
  sentence = 'Manger. Comprendre. Progresser.',
  separator = '. ',
  manualMode = false,
  blurAmount = 5,
  borderColor = '#3A73C1',
  glowColor = 'rgba(58, 115, 193, 0.6)',
  animationDuration = 0.5,
  pauseBetweenAnimations = 1
}) => {
  // Split by separator and keep the separator with each word (except last)
  const parts = sentence.split(separator);
  const words = parts.map((part, index) => {
    if (index < parts.length - 1) {
      return part + '.';
    }
    return part;
  });
  const [currentIndex, setCurrentIndex] = useState(0);
  const [lastActiveIndex, setLastActiveIndex] = useState<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const wordRefs = useRef<(HTMLSpanElement | null)[]>([]);
  const [focusRect, setFocusRect] = useState({ x: 0, y: 0, width: 0, height: 0 });

  useEffect(() => {
    if (!manualMode) {
      const interval = setInterval(
        () => {
          setCurrentIndex(prev => (prev + 1) % words.length);
        },
        (animationDuration + pauseBetweenAnimations) * 1000
      );

      return () => clearInterval(interval);
    }
  }, [manualMode, animationDuration, pauseBetweenAnimations, words.length]);

  useEffect(() => {
    if (currentIndex === null || currentIndex === -1) return;
    if (!wordRefs.current[currentIndex] || !containerRef.current) return;

    // Use requestAnimationFrame to ensure DOM is fully rendered
    const updateFocusRect = () => {
      if (!wordRefs.current[currentIndex] || !containerRef.current) return;
      
      const parentRect = containerRef.current.getBoundingClientRect();
      const activeRect = wordRefs.current[currentIndex].getBoundingClientRect();

      setFocusRect({
        x: activeRect.left - parentRect.left,
        y: activeRect.top - parentRect.top,
        width: activeRect.width,
        height: activeRect.height
      });
    };

    // Small delay to ensure layout is complete, especially in production
    const timeoutId = setTimeout(() => {
      requestAnimationFrame(updateFocusRect);
    }, 50);

    return () => clearTimeout(timeoutId);
  }, [currentIndex, words.length]);

  const handleMouseEnter = (index: number) => {
    if (manualMode) {
      setLastActiveIndex(index);
      setCurrentIndex(index);
    }
  };

  const handleMouseLeave = () => {
    if (manualMode && lastActiveIndex !== null) {
      setCurrentIndex(lastActiveIndex);
    }
  };

  return (
    <div
      className="relative flex gap-2 justify-start items-baseline flex-wrap"
      ref={containerRef}
      style={{ 
        outline: 'none', 
        userSelect: 'none', 
        paddingBottom: '0.5rem', 
        lineHeight: '1.2',
        minHeight: '1.2em' // Prevent layout shift
      }}
    >
      {words.map((word, index) => {
        const isActive = index === currentIndex;
        return (
          <span
            key={index}
            ref={el => { wordRefs.current[index] = el; }}
            className={`relative text-3xl font-semibold tracking-tight sm:text-4xl lg:text-6xl cursor-pointer leading-[1.3] ${
              isActive 
                ? 'bg-gradient-to-r from-[#3A73C1] via-[#6FAFD6] to-[#7ECBC2] bg-clip-text text-transparent' 
                : 'bg-gradient-to-r from-[#3A73C1]/40 via-[#6FAFD6]/40 to-[#7ECBC2]/40 bg-clip-text text-transparent'
            }`}
            style={{
              letterSpacing: '-0.02em',
              paddingBottom: '0.25rem',
              display: 'inline-block',
              filter: manualMode
                ? isActive
                  ? `blur(0px)`
                  : `blur(${blurAmount}px)`
                : isActive
                  ? `blur(0px)`
                  : `blur(${blurAmount}px)`,
              transition: `filter ${animationDuration}s ease, background ${animationDuration}s ease`,
              outline: 'none',
              userSelect: 'none'
            } as React.CSSProperties}
            onMouseEnter={() => handleMouseEnter(index)}
            onMouseLeave={handleMouseLeave}
          >
            {word}
          </span>
        );
      })}

      <motion.div
        className="absolute top-0 left-0 pointer-events-none box-border border-0"
        animate={{
          x: focusRect.x,
          y: focusRect.y,
          width: focusRect.width,
          height: focusRect.height,
          opacity: currentIndex >= 0 && focusRect.width > 0 ? 1 : 0
        }}
        transition={{
          duration: animationDuration,
          ease: "easeInOut"
        }}
        style={{
          '--border-color': borderColor,
          '--glow-color': glowColor
        } as React.CSSProperties}
      >
        <span
          className="absolute w-4 h-4 border-[3px] rounded-[3px] top-[-10px] left-[-10px] border-r-0 border-b-0"
          style={{
            borderColor: 'var(--border-color)',
            filter: 'drop-shadow(0 0 4px var(--border-color))'
          }}
        ></span>
        <span
          className="absolute w-4 h-4 border-[3px] rounded-[3px] top-[-10px] right-[-10px] border-l-0 border-b-0"
          style={{
            borderColor: 'var(--border-color)',
            filter: 'drop-shadow(0 0 4px var(--border-color))'
          }}
        ></span>
        <span
          className="absolute w-4 h-4 border-[3px] rounded-[3px] bottom-[-10px] left-[-10px] border-r-0 border-t-0"
          style={{
            borderColor: 'var(--border-color)',
            filter: 'drop-shadow(0 0 4px var(--border-color))'
          }}
        ></span>
        <span
          className="absolute w-4 h-4 border-[3px] rounded-[3px] bottom-[-10px] right-[-10px] border-l-0 border-t-0"
          style={{
            borderColor: 'var(--border-color)',
            filter: 'drop-shadow(0 0 4px var(--border-color))'
          }}
        ></span>
      </motion.div>
    </div>
  );
};

export default TrueFocus;

