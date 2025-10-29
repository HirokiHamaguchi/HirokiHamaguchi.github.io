import React from 'react';
import { Alert, AlertIcon, AlertDescription } from '@chakra-ui/react';

interface MessageProps {
    message: string;
    type: 'error' | 'win';
}

const Message: React.FC<MessageProps> = ({ message, type }) => {
    const status = type === 'error' ? 'error' : 'success';

    return (
        <Alert status={status} borderRadius="md" w="100%">
            <AlertIcon />
            <AlertDescription>
                {message}
            </AlertDescription>
        </Alert>
    );
};

export default Message;