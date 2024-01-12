const AWS = require("aws-sdk");
const { generateTaxReturnPdf } = require("./PDF");

const s3 = new AWS.S3();

exports.handler = async (event, context) => {
  const parsedEvent = JSON.parse(event.body);
  const [{ contractInfo, participants, receiverInfo, installments }] = parsedEvent.data;
  try {
    const pdfBuffer = await generateTaxReturnPdf({
      contractInfo,
      proposal: {
        installment: installments,
        participants,
        receiverInfo,
      },
    });

    const s3FileName = `${contractInfo.development}.pdf`;

    const s3Params = {
      Bucket: "taxreturns-frontend-storage-73711795134329-staging",
      Key: "public/IR2023/" + s3FileName,
      Body: pdfBuffer,
      ContentType: "application/pdf",
    };
    
    await s3.upload(s3Params).promise();

    console.log(`PDF salvo com sucesso no S3: ${s3Params.Bucket}/${s3Params.Key}`);

    return {
      statusCode: 200,
      body: "deu",
    };
  } catch (pdfBufferError) {
    console.error({ pdfBufferError });
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Erro ao gerar ou salvar o PDF" }),
    };
  }
};
