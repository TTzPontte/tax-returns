const AWS = require("aws-sdk");
const { generateTaxReturnPdf } = require("./PDF");

const s3 = new AWS.S3();

exports.handler = async (event, context) => {
  try {
    const {
      data: {
        getContractInfo: {
          total,
          email,
          development,
          date,
          contractNumber,
          block,
          baseYear,
          balance,
          unit,
          Installments: { items: installments },
          Participants: { items: participants },
        },
      },
    } = event;

    const contractInfo = {
      total,
      email,
      development,
      date,
      contractNumber,
      block,
      baseYear,
      balance,
      unit,
    };

    const receiverInfo = {
      receiver: "MAUÁ CAPITAL REAL ESTATE DEBT III | Investment Multimarket Fund",
      cnpj: "30.982.547/0001-09",
      address: "AV BRIGADEIRO FARIA LIMA, 2277 - SÃO PAULO",
      date: "SÃO PAULO, 05 DE FEVEREIRO DE 2021",
    };

    const environments = ["dev", "staging", "prod"];
    const environment = environments.find(env => process.env.TABLE_NAME.includes(env));

    if (!environment) {
      throw new Error("Nome da tabela não contém DEV, STAGING ou PROD.");
    }

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
    const s3Params = {
      Bucket: s3Bucket,
      Key: `public/IR2023/${s3FileName}`,
      Body: pdfBuffer,
      ContentType: "application/pdf",
    };

    await s3.upload(s3Params).promise();

    console.log(`PDF salvo com sucesso no S3: ${s3Params.Bucket}/${s3Params.Key}`);

    return {
      statusCode: 200,
      body: "Success",
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Erro ao gerar ou salvar o PDF" }),
    };
  }
};
