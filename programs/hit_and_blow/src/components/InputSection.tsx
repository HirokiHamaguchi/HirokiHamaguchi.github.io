import React, { useState, useRef } from 'react';
import {
    Input,
    Button,
    HStack,
    VStack
} from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';

interface InputSectionProps {
    onGuess: (guess: string) => void;
    onReset: () => void;
    disabled: boolean;
}

const InputSection: React.FC<InputSectionProps> = ({ onGuess, onReset, disabled }) => {
    const { t } = useTranslation();
    const [input, setInput] = useState('');
    const inputRef = useRef<HTMLInputElement>(null);

    const handleGuess = () => {
        if (input.trim() && !disabled) {
            onGuess(input.trim());
            setInput('');
            setTimeout(() => {
                inputRef.current?.focus();
            }, 0);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleGuess();
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        // 数字のみ4文字まで制限
        if (/^\d{0,4}$/.test(value)) {
            setInput(value);
        }
    };

    return (
        <VStack spacing={4} w="100%">
            <HStack spacing={4} w="100%" maxW="400px">
                <Input
                    ref={inputRef}
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyPress}
                    placeholder={t('enterGuess')}
                    maxLength={4}
                    isDisabled={disabled}
                    size="lg"
                    textAlign="center"
                    fontSize="xl"
                    letterSpacing="wider"
                    inputMode="numeric"
                    pattern="[0-9]*"
                />
                <Button
                    onClick={handleGuess}
                    isDisabled={disabled || !input.trim()}
                    colorScheme="blue"
                    size="lg"
                >
                    {t('guess')}
                </Button>
            </HStack>
            <Button
                onClick={onReset}
                variant="outline"
                colorScheme="red"
                size="md"
            >
                {t('reset')}
            </Button>
        </VStack>
    );
};

export default InputSection;