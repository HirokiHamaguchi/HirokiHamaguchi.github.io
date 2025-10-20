import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            title: 'Hit and Blow Game',
            gameDescription: 'The secret number consists of four distinct digits from 1 to 9. Enter your 4-digit guess.',
            hitDescription: 'Correct number in correct position',
            blowDescription: 'Correct number in wrong position',
            clearDescription: 'Get all numbers in the correct position to clear! (This game was created for testing purposes on this website.)',
            enterGuess: 'Enter 4 digits',
            guess: 'Guess',
            reset: 'Reset',
            attempts: 'Attempts',
            times: 'times',
            guessHistory: 'Guess History',
            attempt: 'Attempt',
            number: 'Number',
            hit: 'Hit',
            blow: 'Blow',
            congratulations: 'Congratulations! You got it!',
            errorInvalidFormat: 'Please enter exactly 4 digits',
            errorDuplicateDigits: 'Please use 4 different digits',
            errorInvalidDigits: 'Please use digits from 1-9 only',
            languageSwitch: '日本語'
        }
    },
    ja: {
        translation: {
            title: 'Hit and Blow ゲーム',
            gameDescription: '1-9の異なる4つの数字が秘密の番号です。4桁の数字を予想して入力してください。',
            hitDescription: '正しい数字が正しい位置にある',
            blowDescription: '正しい数字が誤った位置にある',
            clearDescription: '全ての数字を正しい位置で当てるとクリアです！ (なお、本ゲームはこのHPにおける動作確認を目的に作成されました。)',
            enterGuess: '4桁入力',
            guess: '予想',
            reset: 'リセット',
            attempts: 'ゲーム回数',
            times: '回',
            guessHistory: '予想履歴',
            attempt: '回数',
            number: '数字',
            hit: 'Hit',
            blow: 'Blow',
            congratulations: 'おめでとうございます！正解です！',
            errorInvalidFormat: '4桁の数字を入力してください',
            errorDuplicateDigits: '異なる4つの数字を使用してください',
            errorInvalidDigits: '1-9の数字のみ使用してください',
            languageSwitch: 'English'
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        lng: 'ja', // default language
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false
        }
    });

export default i18n;