import styled from 'styled-components';

export const NewsContainer = styled.div`
display: flex;
flex-direction: row;
width: 100%;
min-height: 80px;
background-color: #f1f1f1;
margin-bottom: 32px;
padding: 32px;
`;

export const NewsTextBlock = styled.div`
display: flex;
flex-direction: column;
`;

export function News() {
    return (
        <NewsContainer>
            <NewsTextBlock>
                
            </NewsTextBlock>
        </NewsContainer>
    );
}