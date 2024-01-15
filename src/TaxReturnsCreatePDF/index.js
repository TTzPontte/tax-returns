const AWS = require("aws-sdk");
const { generateTaxReturnPdf } = require("./PDF");

const s3 = new AWS.S3();

exports.handler = async (event, context) => {
  const parsedEvent = event;
  const [{ contractInfo, participants, receiverInfo, installments }] =
    parsedEvent.data;

  // Verificar se a variável TABLE_NAME contém "DEV", "STAGING" ou "PROD"
  const environment = process.env.TABLE_NAME.includes("dev")
    ? "dev"
    : process.env.TABLE_NAME.includes("staging")
    ? "staging"
    : process.env.TABLE_NAME.includes("prod")
    ? "prod"
    : (() => {
        console.error("Nome da tabela não contém DEV, STAGING ou PROD.");
        return {
          statusCode: 500,
          body: JSON.stringify({
            error: "Nome da tabela não contém DEV, STAGING ou PROD.",
          }),
        };
      })();

  if (environment instanceof Object) {
    // Se o ambiente não for encontrado, retorne o erro
    return environment;
  }

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

    const s3Bucket =
      environment === "dev"
        ? "taxreturns-frontend-storage-73711795155840-dev"
        : environment === "staging"
        ? "taxreturns-frontend-storage-73711795134329-staging"
        : environment === "prod"
        ? ""
        : "";

        console.log(s3Bucket)

    const s3Params = {
      Bucket: s3Bucket,
      Key: `public/IR2023/${s3FileName}`,
      Body: pdfBuffer,
      ContentType: "application/pdf",
    };

    await s3.upload(s3Params).promise();

    console.log(
      `PDF salvo com sucesso no S3: ${s3Params.Bucket}/${s3Params.Key}`
    );

    return {
      statusCode: 200,
      body: "Success",
    };
  } catch (pdfBufferError) {
    console.error({ pdfBufferError });
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Erro ao gerar ou salvar o PDF" }),
    };
  }
};
