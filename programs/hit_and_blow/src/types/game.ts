export interface GameResult {
    hit: number;
    blow: number;
}

export interface GuessHistory {
    guess: string;
    hit: number;
    blow: number;
    attempt: number;
}

export interface GameState {
    secretNumber: string;
    attempts: number;
    history: GuessHistory[];
    gameWon: boolean;
}

export interface GuessResult {
    success?: boolean;
    error?: string;
    hit?: number;
    blow?: number;
    won?: boolean;
    message?: string;
}