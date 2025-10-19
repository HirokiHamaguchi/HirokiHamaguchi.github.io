import React, { useState } from 'react';
import {
    Box,
    Container,
    VStack,
    Heading,
    Text,
    Badge,
    Flex,
    Button,
    Spacer
} from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { HitAndBlowGame } from '../utils/gameLogic';
import { GuessHistory, GameState } from '../types/game';
import InputSection from './InputSection';
import History from './History';
import Message from './Message';

const Game: React.FC = () => {
    const { t, i18n } = useTranslation();
    const [game] = useState(() => new HitAndBlowGame());
    const [gameState, setGameState] = useState<GameState>({
        secretNumber: '',
        attempts: 0,
        history: [],
        gameWon: false,
    });
    const [errorMessage, setErrorMessage] = useState<string>('');
    const [winMessage, setWinMessage] = useState<string>('');

    const toggleLanguage = () => {
        const currentLang = i18n.language;
        i18n.changeLanguage(currentLang === 'en' ? 'ja' : 'en');
    };

    const handleGuess = (guess: string) => {
        if (gameState.gameWon) return;

        // クライアント側でバリデーション
        let errorKey = '';
        if (guess.length !== 4) {
            errorKey = 'errorInvalidFormat';
        } else if (!/^\d+$/.test(guess) || guess.includes('0')) {
            errorKey = 'errorInvalidDigits';
        } else {
            const uniqueDigits = new Set(guess);
            if (uniqueDigits.size !== 4) {
                errorKey = 'errorDuplicateDigits';
            }
        }

        if (errorKey) {
            setErrorMessage(t(errorKey));
            return;
        }

        const result = game.makeGuess(guess);

        if (result.error) {
            setErrorMessage(result.error);
            return;
        }

        setErrorMessage('');

        if (result.success && result.hit !== undefined && result.blow !== undefined) {
            const newAttempts = gameState.attempts + 1;
            const newHistoryItem: GuessHistory = {
                guess,
                hit: result.hit,
                blow: result.blow,
                attempt: newAttempts,
            };

            const newHistory = [...gameState.history, newHistoryItem];
            const newGameWon = result.won || false;

            setGameState({
                ...gameState,
                attempts: newAttempts,
                history: newHistory,
                gameWon: newGameWon,
            });

            if (result.won) {
                setWinMessage(`${t('congratulations')} (${newAttempts}${t('times')})`);
            }
        }
    };

    const handleReset = () => {
        game.reset();
        setGameState({
            secretNumber: '',
            attempts: 0,
            history: [],
            gameWon: false,
        });
        setErrorMessage('');
        setWinMessage('');
    };

    return (
        <Container maxW="container.md" py={8}>
            <VStack spacing={6}>
                <Flex w="100%" align="center">
                    <Heading as="h2" size="lg" color="blue.600">
                        {t('title')}
                    </Heading>
                    <Spacer />
                    <Button
                        size="sm"
                        variant="outline"
                        onClick={toggleLanguage}
                        colorScheme="blue"
                    >
                        {t('languageSwitch')}
                    </Button>
                </Flex>

                <Box
                    p={6}
                    borderWidth={1}
                    borderRadius="lg"
                    bg="blue.50"
                    w="100%"
                >
                    <Text fontWeight="bold" mb={2}>
                        {t('gameRules')}
                    </Text>
                    <Text mb={2}>
                        {t('gameDescription')}
                    </Text>
                    <Text mb={1}>
                        <Text as="span" fontWeight="bold">Hit</Text>: {t('hitDescription')}
                    </Text>
                    <Text mb={1}>
                        <Text as="span" fontWeight="bold">Blow</Text>: {t('blowDescription')}
                    </Text>
                    <Text>
                        {t('clearDescription')}
                    </Text>
                </Box>

                <InputSection
                    onGuess={handleGuess}
                    onReset={handleReset}
                    disabled={gameState.gameWon}
                />

                <Box textAlign="center">
                    <Text fontSize="lg">
                        {t('attempts')}: <Badge colorScheme="blue" fontSize="md">{gameState.attempts}</Badge> {t('times')}
                    </Text>
                </Box>

                {errorMessage && (
                    <Message message={errorMessage} type="error" />
                )}

                {winMessage && (
                    <Message message={winMessage} type="win" />
                )}

                <Box w="100%">
                    <Heading as="h3" size="md" mb={4} textAlign="center">
                        {t('guessHistory')}
                    </Heading>
                    <History history={gameState.history} />
                </Box>
            </VStack>
        </Container>
    );
};

export default Game;