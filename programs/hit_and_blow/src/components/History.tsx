import React from 'react';
import {
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableContainer,
    Text,
    Badge
} from '@chakra-ui/react';
import { useTranslation } from 'react-i18next';
import { GuessHistory } from '../types/game';

interface HistoryProps {
    history: GuessHistory[];
}

const History: React.FC<HistoryProps> = ({ history }) => {
    const { t } = useTranslation();

    if (history.length === 0) {
        return (
            <Text textAlign="center" color="gray.500" py={8}>
                No guesses yet
            </Text>
        );
    }

    // 最新の予想から順に表示
    const sortedHistory = [...history].reverse();

    return (
        <TableContainer>
            <Table variant="simple" size="md">
                <Thead>
                    <Tr>
                        <Th textAlign="center">{t('attempt')}</Th>
                        <Th textAlign="center">{t('number')}</Th>
                        <Th textAlign="center">{t('hit')}</Th>
                        <Th textAlign="center">{t('blow')}</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {sortedHistory.map((item) => (
                        <Tr key={item.attempt}>
                            <Td textAlign="center">
                                <Badge colorScheme="blue">{item.attempt}</Badge>
                            </Td>
                            <Td textAlign="center">
                                <Text fontSize="lg" fontWeight="bold" letterSpacing="wider">
                                    {item.guess}
                                </Text>
                            </Td>
                            <Td textAlign="center">
                                <Badge colorScheme="green" fontSize="md">
                                    {item.hit}
                                </Badge>
                            </Td>
                            <Td textAlign="center">
                                <Badge colorScheme="orange" fontSize="md">
                                    {item.blow}
                                </Badge>
                            </Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
        </TableContainer>
    );
};

export default History;