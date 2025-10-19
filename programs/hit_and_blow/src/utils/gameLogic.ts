import { GameResult, GuessResult } from '../types/game';

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
            return '4桁の数字を入力してください。';
        }

        if (!/^\d+$/.test(guess)) {
            return '数字のみを入力してください。';
        }

        if (guess.includes('0')) {
            return '0は使用できません。1-9の数字を使用してください。';
        }

        const uniqueDigits = new Set(guess);
        if (uniqueDigits.size !== 4) {
            return '同じ数字を重複して使用することはできません。';
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
                message: `おめでとうございます！正解しました！`
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