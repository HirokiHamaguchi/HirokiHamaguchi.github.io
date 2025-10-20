import { GameResult, GuessResult } from '../types/game';
import i18n from '../i18n';

export class HitAndBlowGame {
    private secretNumber: string;

    constructor() {
        this.secretNumber = this.generateSecretNumber();
    }

    private generateSecretNumber(): string {
        const digits = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        let result = '';

        for (let i = 0; i < 4; i++) {
            const randomIndex = Math.floor(Math.random() * digits.length);
            result += digits[randomIndex];
            digits.splice(randomIndex, 1);
        }

        return result;
    }

    validateGuess(guess: string): string | null {
        if (guess.length !== 4) {
            return i18n.t('errorInvalidFormat');
        }

        if (!/^\d+$/.test(guess)) {
            return i18n.t('errorInvalidDigits');
        }

        if (guess.includes('0')) {
            return i18n.t('errorInvalidDigits');
        }

        const uniqueDigits = new Set(guess);
        if (uniqueDigits.size !== 4) {
            return i18n.t('errorDuplicateDigits');
        }

        return null;
    }

    calculateHitAndBlow(guess: string): GameResult {
        let hit = 0;
        let blow = 0;

        for (let i = 0; i < 4; i++) {
            if (guess[i] === this.secretNumber[i]) {
                hit++;
            } else if (this.secretNumber.includes(guess[i])) {
                blow++;
            }
        }

        return { hit, blow };
    }

    makeGuess(guess: string): GuessResult {
        const validationError = this.validateGuess(guess);
        if (validationError) {
            return { error: validationError };
        }

        const result = this.calculateHitAndBlow(guess);

        if (result.hit === 4) {
            return {
                success: true,
                hit: result.hit,
                blow: result.blow,
                won: true,
                message: i18n.t('congratulations')
            };
        }

        return {
            success: true,
            hit: result.hit,
            blow: result.blow,
            won: false
        };
    }

    getSecretNumber(): string {
        return this.secretNumber;
    }

    reset(): void {
        this.secretNumber = this.generateSecretNumber();
    }
}